from datetime import datetime

from pydantic import BaseModel


class GetMessageResponse(BaseModel):
    content: str
    send_time: datetime
    sender_type: str
    chatroom_id: int

class SendMessageResponse(BaseModel):
    content: str
    send_time: datetime
    sender_type: str
    chatroom_id: int
