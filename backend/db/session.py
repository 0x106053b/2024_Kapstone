from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL
)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()