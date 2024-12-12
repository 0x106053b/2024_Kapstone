from pydantic import BaseModel

class ChatroomRequest(BaseModel):
    chatroom_id: int

class CreateChatroomRequest(BaseModel):
    chatroom_name: str
    instructor_name: str
    course_code: str