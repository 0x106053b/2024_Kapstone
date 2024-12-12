import pytest
from httpx import AsyncClient
from sqlalchemy import text
from backend.api.auth import authenticate_user
from backend.main import app
from backend.schema.jwt.response_model import Payload
from backend.schema.models import User
from backend.test.conftest import TestingSessionLocal

@pytest.mark.asyncio
async def test_create_user():
    payload = {
        "first_name": "test",
        "last_name": "man",
        "email": "test@gmail.com",
        "password": "test1234"
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/user/register", json=payload)

    assert response.status_code == 201

    async with TestingSessionLocal() as session:
        stored_user = await session.execute(
            text("select * from user where email = :email"), {"email": payload["email"]}
        )
        stored_user = stored_user.fetchone()

    assert stored_user is not None
    assert stored_user.password != payload["password"]
    assert response.json()["user_id"] == 1


@pytest.mark.asyncio
async def test_find_user():

    async def mock_authenticate_user():
        return Payload(user_id=1)

    app.dependency_overrides[authenticate_user] = mock_authenticate_user

    async with TestingSessionLocal() as session:
        new_user = User(
            first_name="test",
            last_name="man",
            email="test@gmail.com",
            password="test1234"
        )
        session.add(new_user)
        await session.commit()

    headers = {"Authorization": "Bearer fake_jwt_token"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/user/", headers=headers)

    assert response.status_code == 200
    assert response.json()["first_name"] == "test"
    assert response.json()["last_name"] == "man"
    assert response.json()["email"] == "test@gmail.com"