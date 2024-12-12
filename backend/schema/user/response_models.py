from pydantic import BaseModel


class UserResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str

class UserCreateResponse(BaseModel):
    user_id: int