from datetime import datetime, timedelta, timezone
from typing import Union
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request, HTTPException, status
from jose import jwt, ExpiredSignatureError, JWTError
from jwt import InvalidTokenError, DecodeError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from backend.db.session import get_db
from backend.exception.auth_exception import CredentialError, TokenExpiredError
from backend.schema.jwt.response_model import TokenResponse, Payload
from backend.schema.models import User
from backend.schema.user.request_models import UserLoginRequest

import os
import bcrypt
from redis.asyncio import Redis

router = APIRouter()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
ACCESS_TOKEN_COOKIE_EXPIRE_TIME = 1800
REFRESH_TOKEN_COOKIE_EXPIRE_TIME = 604800

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

redis_client = Redis(host='localhost', port=6379, decode_responses=True)

@router.post("/login", response_model=TokenResponse, tags=["auth"])
async def login(user_request: UserLoginRequest,
                response: Response,
                db: AsyncSession = Depends(get_db)):
    # Read user from db by email
    result = await db.execute(select(User).where(user_request.email == User.email))
    user = result.scalars().first()

    # Authenticate user email & password
    if user and is_valid_password(user, user_request.password):
        user_id = str(user.user_id)

        # Create access token
        claim = {
            "sub": user_id
        }
        access_token = create_access_token(
            claim,
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_refresh_token(
            {"sub": user_id},
            timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
        await store_refresh_token(user_id, refresh_token)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid user info")

@router.post("/refresh-token", tags=["auth"])
async def refresh(request: Request):
    refresh_token = extract_token_from_header(request)
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise CredentialError()

        found_token = await get_refresh_token(user_id)
        if found_token != refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

        claim = {
            "sub": str(user_id)
        }
        new_access_token = create_access_token(
            claim,
            expires_delta=timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            ))

        return {
            "access_token": new_access_token
        }

    except ExpiredSignatureError:
        raise TokenExpiredError()
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed token")

def extract_token_from_header(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise CredentialError()
    token = auth_header.split(" ")[1]
    return token

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def store_refresh_token(user_id: str, refresh_token: str):
    await redis_client.setex(
        name=f"refresh_token:{user_id}",
        value=refresh_token,
        time=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

async def get_refresh_token(user_id: str):
    refresh_token = await redis_client.get(f"refresh_token:{user_id}")
    return refresh_token

def verify_refresh_token(found_token: str, refresh_token: str):
    if found_token == refresh_token:
        return True
    else:
        return False

def authenticate_user(request: Request):
    token = extract_token_from_header(request)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = payload.get("sub")
        if not user_id:
            raise CredentialError()
    except InvalidTokenError:
        raise CredentialError()
    except ExpiredSignatureError:
        raise TokenExpiredError()
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    return Payload(
        user_id=int(payload.get("sub"))
    )


def is_valid_password(user: Union[User, None], password: str) -> bool:
    bytes_password = password.encode('utf-8')
    hashed_password = user.password.encode('utf-8')
    if bcrypt.checkpw(bytes_password, hashed_password):
        return True
    return False