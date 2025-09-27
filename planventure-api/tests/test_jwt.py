import pytest
import jwt
from datetime import datetime, timedelta
from utils.security.jwt import (
    create_access_token,
    create_refresh_token,
    verify_token,
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
)


def test_access_token_creation():
    """Test creation and verification of access tokens."""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)

    # Verify token
    payload = verify_token(token)
    assert payload["sub"] == "test@example.com"
    assert payload["type"] == "access"
    assert "exp" in payload


def test_refresh_token_creation():
    """Test creation and verification of refresh tokens."""
    data = {"sub": "test@example.com"}
    token = create_refresh_token(data)

    # Verify token
    payload = verify_token(token)
    assert payload["sub"] == "test@example.com"
    assert payload["type"] == "refresh"
    assert "exp" in payload


def test_token_expiration():
    """Test token expiration."""
    data = {"sub": "test@example.com"}
    token = create_access_token(data, expires_delta=timedelta(seconds=-1))

    with pytest.raises(jwt.ExpiredSignatureError):
        verify_token(token)


def test_invalid_token():
    """Test invalid token handling."""
    with pytest.raises(jwt.InvalidTokenError):
        verify_token("invalid.token.string")
