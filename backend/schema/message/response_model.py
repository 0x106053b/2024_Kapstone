from datetime import datetime

from pydantic import BaseModel


class GetMessageResponse(BaseModel):
    message_id: int
    content: str
    send_time: datetime
    sender_type: str
    chatroom_id: int

class SendMessageResponse(BaseModel):
    message_id: int
    content: str
    send_time: datetime
    sender_type: str
    chatroom_id: int
