from datetime import datetime

from pydantic import BaseModel

class GetDocumentRequest(BaseModel):
    document_id: int
    document_name: str
    uploaded_time: datetime


class DeleteDocumentRequest(BaseModel):
    document_id: int