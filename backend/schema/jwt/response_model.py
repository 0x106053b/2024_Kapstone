from typing import Union

from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str

class Payload(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str