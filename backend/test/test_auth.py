from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from backend.api.auth import login
from backend.main import app
from backend.schema.jwt.response_model import TokenResponse
from backend.schema.user.request_models import UserCreateRequest, UserLoginRequest

client = TestClient(app)

@patch("backend.db.session.get_db")
def test_login_giving_access_token(mock_db):

    mock_session = MagicMock()
    mock_db.return_value = mock_session

    user = UserCreateRequest(
        first_name="Ben",
        last_name="Rhee",
        email="br@gmail.com",
        password="br12345678"
    )

    user_request = UserLoginRequest(
        email="br@gmail.com",
        password="br12345678"
    )

    login_response = login(user_request=user_request, db=mock_session)