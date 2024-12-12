from datetime import datetime, timedelta, timezone
from typing import Union, Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request, HTTPException, status
from jose import jwt, ExpiredSignatureError, JWTError
from jwt import InvalidTokenError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.schema.jwt.response_model import TokenResponse, Payload
from backend.schema.models import User
from backend.schema.user.request_models import UserLoginRequest

import os
import bcrypt

router = APIRouter()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

expired_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Expired access token",
    headers={"WWW-Authenticate": "Bearer"}
)

@router.post("/login", response_model=TokenResponse, tags=["auth"])
async def login(user_request: UserLoginRequest,
                db: AsyncSession = Depends(get_db)):
    # Read user from db by email
    result = await db.execute(select(User).where(user_request.email == User.email))
    user = result.scalars().first()

    # Authenticate user email & password
    if user and is_valid_password(user, user_request.password):

        # Create access token
        claim = {
            "sub": str(user.user_id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        access_token = create_access_token(claim, timedelta(minutes=30))
        return TokenResponse(
            access_token=access_token
        )
    return False

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if token is None:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id, email, first_name, last_name = (
            payload.get("sub"),
            payload.get("email"),
            payload.get("first_name"),
            payload.get("last_name")
        )
        if not all([user_id, email, first_name, last_name]):
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise expired_token_exception
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    return Payload(
        user_id=int(payload.get("sub")),
        first_name=payload.get("first_name"),
        last_name=payload.get("last_name"),
        email=payload.get("email")
    )


def is_valid_password(user: Union[User, None], password: str) -> bool:
    bytes_password = password.encode('utf-8')
    hashed_password = user.password.encode('utf-8')
    if bcrypt.checkpw(bytes_password, hashed_password):
        return True
    return False