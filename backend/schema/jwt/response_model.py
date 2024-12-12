from typing import Union

from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class Payload(BaseModel):
    user_id: int