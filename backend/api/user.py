from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi_mail import MessageSchema, FastMail
from pydantic import validate_email
from pydantic_core import PydanticCustomError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from backend.api.auth import authenticate_user
from backend.db.session import get_db
from backend.schema.jwt.response_model import Payload
from backend.schema.models import User
from backend.schema.user.request_models import UserCreateRequest
from backend.schema.user.response_models import UserCreateResponse, UserResponse
from typing import List
import bcrypt
from backend.utils.mail_config import conf

router = APIRouter()

@router.get("/", response_model=UserResponse, tags=["user"])
async def find_user(
        db: AsyncSession = Depends(get_db),
        current_user: Payload = Depends(authenticate_user)):
    result = await db.execute(select(User).where(current_user.user_id == User.user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find the user")
    return user

@router.post("/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED, tags=["user"])
async def create_user(user_request: UserCreateRequest, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)): # CREATE USER
    hashed_password = hash_password(user_request.password)  # Hashing
    new_user = User(
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        email=user_request.email,
        password=hashed_password
    )

    try:
        validate_email(user_request.email)
        result = await db.execute(select(User).where(new_user.email == User.email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exists")
        # background_tasks.add_task(send_email, user.email)

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user) # refresh session to ensure the instance is updated

    except PydanticCustomError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid email format")
    except DataError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid data format")

    return new_user


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

async def send_email(to_email: str):
    subject = "[Perfectstdm: Confirmation email]"
    body = "Hi, this is Perfectstdm.\n We need your confirmation to your email address, please type in the following code to the form.\n Thank you."
    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=body,
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)