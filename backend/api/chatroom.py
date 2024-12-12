from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select, delete, update
from sqlalchemy.exc import DataError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from backend.api.auth import authenticate_user
from backend.db.session import get_db
from backend.schema.chatroom.request_model import CreateChatroomRequest, ChatroomRequest, UpdateChatroomRequest
from backend.schema.chatroom.response_model import CreateChatroomResponse, ChatroomResponse, UpdateChatroomResponse
from backend.schema.jwt.response_model import Payload
from backend.schema.models import Chatroom

router = APIRouter()

@router.post("/create", response_model=CreateChatroomResponse,
             status_code=status.HTTP_201_CREATED,
             tags=["chatroom"])
async def create_chatroom(chatroom_request: CreateChatroomRequest,
                          db: AsyncSession = Depends(get_db),
                          current_user: Payload = Depends(authenticate_user)):

    chatroom = Chatroom(
        chatroom_name=chatroom_request.chatroom_name,
        instructor_name=chatroom_request.instructor_name,
        course_code=chatroom_request.course_code,
        user_id=current_user.user_id
    )

    try:
        db.add(chatroom)
        await db.commit()
        await db.refresh(chatroom)
    except DataError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="data too long")
    return chatroom

@router.get("/", response_model=List[ChatroomResponse], tags=["chatroom"])
async def find_all_chatroom(db: AsyncSession = Depends(get_db),
                            current_user: Payload = Depends(authenticate_user)):
    result = await db.execute(select(Chatroom).where(current_user.user_id == Chatroom.user_id))
    chatrooms = result.scalars().all()
    return chatrooms

@router.get("/{chatroom_id}", response_model=ChatroomResponse, tags=["chatroom"])
async def find_chatroom(chatroom_id: int,
                        db: AsyncSession = Depends(get_db),
                        current_user: Payload = Depends(authenticate_user)):
    result = await db.execute(select(Chatroom).
                              where(chatroom_id == Chatroom.chatroom_id,
                                    current_user.user_id == Chatroom.user_id))
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
                          current_user: Payload = Depends(authenticate_user)):
    result = await db.execute(delete(Chatroom).where(chatroom_id == Chatroom.chatroom_id,
                                                     current_user.user_id == Chatroom.user_id))

    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to delete the chatroom")
    await db.commit()
    return {
        "message": "Chatroom deleted successfully"
    }

@router.patch("/{chatroom_id}", response_model=UpdateChatroomResponse, tags=["chatroom"])
async def update_chatroom(chatroom_id: int,
                          chatroom_request: UpdateChatroomRequest,
                          db: AsyncSession = Depends(get_db),
                          current_user: Payload = Depends(authenticate_user)):
    update_data = chatroom_request.model_dump(exclude_unset=True)
    result = await db.execute(select(Chatroom)
                              .where(chatroom_id == Chatroom.chatroom_id,
                                                     current_user.user_id == Chatroom.user_id))

    chatroom = result.scalars().first()

    if chatroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unable to load chatroom"
        )

    for key, val in update_data.items():
        setattr(chatroom, key, val)

    await db.commit()
    await db.refresh(chatroom)

    return chatroom