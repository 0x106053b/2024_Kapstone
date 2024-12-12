from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from backend.api.auth import get_current_user_from_cookie
from backend.db.session import get_db
from backend.schema.chatroom.request_model import CreateChatroomRequest, ChatroomRequest
from backend.schema.chatroom.response_model import CreateChatroomResponse, ChatroomResponse
from backend.schema.jwt.response_model import Payload
from backend.schema.models import Chatroom

router = APIRouter()

@router.post("/create", response_model=CreateChatroomResponse, status_code=status.HTTP_201_CREATED, tags=["chatroom"])
async def create_chatroom(chatroom_request: CreateChatroomRequest,
                    db: AsyncSession = Depends(get_db),
                    current_user: Payload = Depends(get_current_user_from_cookie)):
    chatroom = Chatroom(
        chatroom_name=chatroom_request.chatroom_name,
        instructor_name=chatroom_request.instructor_name,
        course_code=chatroom_request.course_code,
        user_id=current_user.user_id
    )
    db.add(chatroom)
    await db.commit()
    await db.refresh(chatroom)
    return chatroom

@router.get("/", response_model=List[ChatroomResponse], tags=["chatroom"])
async def find_all_chatroom(db: AsyncSession = Depends(get_db),
                      current_user: Payload = Depends(get_current_user_from_cookie)):
    result = await db.execute(select(Chatroom).where(current_user.user_id == Chatroom.user_id))
    chatrooms = result.scalars().all()
    return chatrooms

@router.get("/{chatroom_id}", response_model=ChatroomResponse, tags=["chatroom"])
async def find_chatroom(chatroom_id: int,
                        db: AsyncSession = Depends(get_db),
                        current_user: Payload = Depends(get_current_user_from_cookie)):
    result = await db.execute(select(Chatroom).where(chatroom_id == Chatroom.chatroom_id, current_user.user_id == Chatroom.user_id))
    chatroom = result.scalars().first()
    if chatroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to load chatroom"
        )
    return chatroom

@router.delete("/{chatroom_id}", tags=["chatroom"])
async def delete_chatroom(chatroom_id: int,
                          db: AsyncSession = Depends(get_db),
                          current_user: Payload = Depends(get_current_user_from_cookie)):
    result = await db.execute(delete(Chatroom).where(chatroom_id == Chatroom.chatroom_id, current_user.user_id == Chatroom.user_id))
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to delete the chatroom")
    return {
        "message": "Chatroom deleted successfully"
    }


# send to model

# message authorization
# document authorization