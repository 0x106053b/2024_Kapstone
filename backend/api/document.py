import uuid
from datetime import datetime
from typing import List
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
import os

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.api.auth import get_current_user_from_cookie
from backend.db.session import get_db
from backend.schema.document.request_model import DeleteDocumentRequest, GetDocumentRequest
from backend.schema.jwt.response_model import Payload
from backend.schema.models import Document, Chatroom

load_dotenv()

router = APIRouter()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY_ID")
S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")

s3_client = boto3.client(
    "s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# upload document
@router.post("/{chatroom_id}", tags=["document"])
async def upload_document(chatroom_id: int,
                          files: List[UploadFile] = File(...),
                          db: AsyncSession = Depends(get_db),
                          current_user: Payload = Depends(get_current_user_from_cookie)):
    result = await db.execute(
        select(Chatroom).where(chatroom_id == Chatroom.chatroom_id, current_user.user_id == Chatroom.user_id))
    chatroom = result.scalars().first()
    if chatroom is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unable access the chatroom")

    uploaded_documents = []

    try:
        for file in files:
            s3_key = f"{uuid.uuid4()}-{file.filename}"
            s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
            s3_client.upload_fileobj(
                file.file,
                S3_BUCKET_NAME,
                s3_key
            )
            document = Document(
                document_name=file.filename,
                uploaded_name=s3_key,
                s3_url=s3_url,
                uploaded_time=datetime.now(),
                chatroom_id=chatroom_id
            )
            db.add(document)
            uploaded_documents.append(document)
        await db.commit()
        for document in uploaded_documents:
            await db.refresh(document)
        return {
            "chatroom_id": chatroom_id,
            "uploaded_files": [
                {"document_id": document.document_id,
                 "document_name": document.document_name,
                 "uploaded_name": document.uploaded_name,
                 "uploaded_time": document.uploaded_time,
                 "s3_url": document.s3_url
                 } for document in uploaded_documents
            ]
        }
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"S3 upload fails: {str(e)}")


@router.delete("/{chatroom_id}/{document_id}", tags=["document"])
async def delete_document(chatroom_id: int,
                          document_id: int,
                          db: AsyncSession = Depends(get_db),
                          current_user: Payload = Depends(get_current_user_from_cookie)):
    try:
        result = await db.execute(
            select(Chatroom).where(chatroom_id == Chatroom.chatroom_id, current_user.user_id == Chatroom.user_id))
        chatroom = result.scalars().first()
        if chatroom is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unable to access the chatroom ")
        result = await db.execute(
            select(Document).where(document_id == Document.document_id, chatroom_id == Document.chatroom_id))
        document = result.scalars().first()
        if document is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=document.uploaded_name)

        await db.delete(document)
        await db.commit()

        return {"message": "Document deleted successfully"}

    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"S3 delete fails: {str(e)}")


@router.get("/{chatroom_id}", response_model=List[GetDocumentRequest], tags=["document"])
async def get_documents(chatroom_id: int,
                        db: AsyncSession = Depends(get_db),
                        current_user: Payload = Depends(get_current_user_from_cookie)):
    result = await db.execute(select(Chatroom).where(chatroom_id == Chatroom.chatroom_id, current_user.user_id == Chatroom.user_id))
    chatroom = result.scalars().first()
    if chatroom is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unable to load the documents")
    result = await db.execute(select(Document).where(chatroom_id == Document.chatroom_id))
    documents = result.scalars().all()
    return documents