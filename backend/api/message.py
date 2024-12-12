from datetime import datetime
from typing import List

from cachetools import TTLCache
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from ai.ChatBot import ChatBot
from backend.api.auth import authenticate_user
from backend.db.session import get_db
from backend.exception.chatroom_exception import ChatroomNotFoundError, ChatroomForbiddenError
from backend.exception.message_exception import ChatbotResponseError
from backend.schema.jwt.response_model import Payload
from backend.schema.message.request_model import SendMessageRequest
from backend.schema.message.response_model import SendMessageResponse, GetMessageResponse
from backend.schema.models import Message, Chatroom

router = APIRouter()

chat_sessions = TTLCache(maxsize=1000, ttl=3600)

@router.post("/{chatroom_id}", response_model=SendMessageResponse, tags=["message"])
async def send_message_to_model(chatroom_id: int, user_request: SendMessageRequest,
                                db: AsyncSession = Depends(get_db),
                                current_user: Payload = Depends(authenticate_user)):

    result = await db.execute(select(Chatroom)
                              .where(chatroom_id == Chatroom.chatroom_id)
                              .options(joinedload(Chatroom.message)))
    chatroom = result.scalars().first()

    if chatroom is None:
        raise ChatroomNotFoundError()
    if chatroom.user_id != current_user.user_id:
        raise ChatroomForbiddenError()

    # save user message to db
    message_content = user_request.content
    user_message = Message(
        content=message_content,
        send_time=datetime.now(),
        sender_type="user",
        chatroom_id=chatroom_id
    )
    chat_json = {"question": message_content, "answer": ""}
    db.add(user_message)

    bot = chat_sessions.get(chatroom_id)
    if not bot:
        bot = ChatBot(
            user_id=current_user.user_id,
            course_id=chatroom_id
        )
        chatting_context = chatroom.message[-6:]
        for i, message in enumerate(chatting_context):
            if message.sender_type == "user":
                chat_json = {"question": message.content, "answer": ""}
                if i + 1 < len(chatting_context) and chatting_context[i+1].sender_type == "bot":
                    chat_json["answer"] = chatting_context[i+1].content
                bot.chat_history.append(chat_json)

        chat_sessions[chatroom_id] = bot

    # get response from the model
    try:
        bot_response = bot.answer(user_message.content)
        chat_json["answer"] = bot_response
        bot.chat_history.append(chat_json)
    except Exception as e:
        raise ChatbotResponseError(e)

    # save the response to db
    bot_message = Message(
        content=bot_response,
        send_time=datetime.now(),
        sender_type="bot",
        chatroom_id=chatroom_id
    )
    db.add(bot_message)
    await db.commit()
    await db.refresh(user_message)
    await db.refresh(bot_message)

    # send back response from the model

    return bot_message

@router.get("/{chatroom_id}", response_model=List[GetMessageResponse], tags=['message'])
async def get_message(chatroom_id,
                      db: AsyncSession = Depends(get_db),
                      current_user: Payload = Depends(authenticate_user)):
    result = await db.execute(select(Chatroom).
                              where(chatroom_id == Chatroom.chatroom_id,
                                    current_user.user_id == Chatroom.user_id))
    chatroom = result.scalars().first()
    if chatroom is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unable to load the messages")
    result = await db.execute(select(Message).where(chatroom_id == Message.chatroom_id))
    message = result.scalars().all()
    return message

@router.delete("/{chatroom_id}", tags=['message'])
async def delete_message(
        chatroom_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: Payload = Depends(authenticate_user)):
    result = await db.execute(delete(Message).where(chatroom_id == Message.chatroom_id))

    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await db.commit()

    return {
        "message": "Messages deleted successfully"
    }

@router.delete("/{chatroom_id}/{message_id}", tags=['message'])
async def delete_message(
        chatroom_id: int,
        message_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: Payload = Depends(authenticate_user)):
    result = await db.execute(delete(Message).where(chatroom_id == Message.chatroom_id,
                                                    message_id == Message.message_id))
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await db.commit()

    return {
        "message": "Message deleted successfully"
    }



