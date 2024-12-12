from fastapi import HTTPException

class ChatbotResponseError(HTTPException):
    def __init__(self, detail: str = "Failed to get a response from the chatbot"):
        super().__init__(status_code=500, detail=detail)