from datetime import datetime, timedelta, timezone
import jwt
from typing import Dict, Optional

# Configuration constants
JWT_SECRET_KEY = "your-secret-key"  # Move to environment variables in production
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    Args:
        data: Dictionary containing claims
        expires_delta: Optional expiration time
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(data: Dict) -> str:
    """Create a refresh token with longer expiration."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Dict:
    """
    Verify and decode a JWT token.
    Args:
        token: JWT token string
    Returns:
        Decoded token payload
    Raises:
        jwt.InvalidTokenError: If token is invalid
    """
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
