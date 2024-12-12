from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.api.auth import get_current_user_from_cookie
from backend.db.session import get_db
from backend.schema.jwt.response_model import Payload
from backend.schema.models import User
from backend.schema.user.request_models import UserCreateRequest, UserLoginRequest
from backend.schema.user.response_models import UserCreateResponse, UserResponse
from sqlalchemy.orm import Session
from typing import List
import bcrypt

router = APIRouter()

@router.get("/", response_model=List[UserResponse], tags=["user"])
async def find_users(db: AsyncSession = Depends(get_db)): # GET USERS
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.get("/{user_id}", response_model=UserResponse, tags=["user"])
async def find_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: Payload = Depends(get_current_user_from_cookie)):
    if user_id == current_user.user_id:
        result = await db.execute(select(User).where(user_id == User.user_id))
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find the user")
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials")
@router.post("/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED, tags=["user"])
async def create_user(user_request: UserCreateRequest, db: AsyncSession = Depends(get_db)): # CREATE USER
    hashed_password = hash_password(user_request.password)  # Hashing
    user = User(
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        email=user_request.email,
        password=hashed_password
    )
    db.add(user)
    await db.commit()
    await db.refresh(user) # refresh session to ensure the instance is updated
    return user


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

