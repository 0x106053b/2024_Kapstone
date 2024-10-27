from datetime import datetime
from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from backend.api.auth import get_current_user_from_cookie
from backend.db.session import get_db
from backend.schema.jwt.response_model import Payload
from backend.schema.message.request_model import SendMessageRequest, GetMessageRequest
from backend.schema.message.response_model import SendMessageResponse, GetMessageResponse
from backend.schema.models import Message

router = APIRouter()

@router.post("/", response_model=SendMessageResponse, tags=["message"])
async def send_message_to_model(user_request: SendMessageRequest,
                                db: AsyncSession = Depends(get_db),
                                current_user: Payload = Depends(get_current_user_from_cookie)):
    # save user message to db
    message_content, chatroom_id = user_request.content, user_request.chatroom_id
    user_message = Message(
        content=message_content,
        send_time=datetime.now(),
        sender_type="user",
        chatroom_id=chatroom_id
    )
    db.add(user_message)
    await db.commit()
    await db.refresh(user_message)

    # send the request to the model

    # get response from the model
    fake_response = "Hi, I'm your studymate stdm! How may I help you? ^_^"

    # save the response to db
    bot_message = Message(
        content=fake_response,
        send_time=datetime.now(),
        sender_type="bot",
        chatroom_id=chatroom_id
    )
    db.add(bot_message)
    await db.commit()
    await db.refresh(bot_message)

    # send back response from the model

    return bot_message

@router.get("/", response_model=List[GetMessageResponse], tags=['message'])
async def get_message(message_request: GetMessageRequest,
                db: AsyncSession = Depends(get_db),
                current_user: Payload = Depends(get_current_user_from_cookie)):
    result = await db.execute(select(Message).where(message_request.chatroom_id == Message.chatroom_id))
    message = result.scalars().all()
    return message
