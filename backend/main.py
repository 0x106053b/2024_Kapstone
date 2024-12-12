import os

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from backend.api import user, auth, chatroom, message, document
from backend.db.session import engine, Base
import logging

app = FastAPI()

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# @app.on_event("startup")
# async def on_startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log basic request information
    logger.info(f"Request: {request.method} {request.url} {request.headers}")
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Error during {request.method} {request.url}: {str(e)}")
        raise


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", os.getenv("NGROK_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chatroom.router, prefix="/chatroom", tags=["chatroom"])
app.include_router(message.router, prefix="/message", tags=["message"])
app.include_router(document.router, prefix="/document", tags=["document"])