from pydantic import BaseModel


class CreateChatroomResponse(BaseModel):
    chatroom_id: int

class ChatroomResponse(BaseModel):
    chatroom_id: int
    chatroom_name: str
    course_code: str
    instructor_name: str