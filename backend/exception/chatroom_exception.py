from fastapi import HTTPException

class ChatroomNotFoundError(HTTPException):
    def __init__(self, detail: str = "The chatroom does not exist"):
        super().__init__(status_code=404, detail=detail)

class ChatroomForbiddenError(HTTPException):
    def __init__(self, detail: str = "Access to the chatroom is forbidden"):
        super().__init__(status_code=403, detail=detail)