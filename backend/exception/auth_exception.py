from fastapi import HTTPException

class CredentialError(HTTPException):
    def __init__(self, detail="Could not validate credentials"):
        super().__init__(status_code=401,
                         detail=detail,
                         headers={"WWW-Authenticate": "Bearer"})

class TokenExpiredError(HTTPException):
    def __init__(self, detail="Expired access token"):
        super().__init__(status_code=401,
                         detail=detail,
                         headers={"WWW-Authenticate": "Bearer"})