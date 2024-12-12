from typing import Optional

from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    password: str

class UserLoginRequest(BaseModel):
    email: str
    password: str