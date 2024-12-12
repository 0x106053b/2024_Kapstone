from pydantic import BaseModel

class UploadDocumentResponse(BaseModel):
    document_id: int
    file_name: str
    s3_url: str