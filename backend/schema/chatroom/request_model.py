from typing import Optional

from pydantic import BaseModel

class ChatroomRequest(BaseModel):
    chatroom_id: int

class CreateChatroomRequest(BaseModel):
    chatroom_name: str
    instructor_name: str
    course_code: str

class UpdateChatroomRequest(BaseModel):
    chatroom_name: Optional[str] = None
    instructor_name: Optional[str] = None
    course_code: Optional[str] = None