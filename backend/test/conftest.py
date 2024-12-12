import pytest
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.db.session import get_db, Base
from backend.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args = {
        "check_same_thread": False
    },
    poolclass=StaticPool
)
TestingSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function", autouse=True)
async def setup_and_teardown_db():
    # Create the database schema before each test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # Run the test

    # Drop the database schema after the test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)