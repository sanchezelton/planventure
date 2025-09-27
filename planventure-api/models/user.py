import re
from typing import Dict
from .base import BaseModel, db
from datetime import datetime, timezone
from utils.security import hash_password, verify_password
from utils.security.jwt import create_access_token, create_refresh_token, verify_token


class User(BaseModel):
    """User model for authentication and user management."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    password_salt = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Add relationship
    trips = db.relationship("Trip", back_populates="user", lazy="dynamic")

    def __repr__(self):
        """Returns a string representation of the User object."""
        return f"<User {self.email}>"

    def __init__(self, email, password):
        """Initializes a User instance with email and hashed password."""
        super().__init__()
        if not self.validate_email(email):
            raise ValueError("Invalid email format")
        self.email = email
        self.__init_password(password)
        self.is_active = True

    def __init_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash, self.password_salt = hash_password(password)

    def set_password(self, password):
        """Hashes the password and updates it."""
        self.password_hash, self.password_salt = hash_password(password)
        self.updated_at = datetime.now(timezone.utc)

    def authenticate(self, password: str) -> bool:
        """Verify the provided password against stored hash."""
        return verify_password(password, self.password_hash)

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validates an email address format.
        Returns True if valid, False otherwise.
        """
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(email_pattern, email))

    def generate_auth_tokens(self) -> Dict[str, str]:
        """Generate access and refresh tokens for the user."""
        tokens = {
            "access_token": create_access_token({"sub": self.email}),
            "refresh_token": create_refresh_token({"sub": self.email}),
            "token_type": "bearer",
        }
        return tokens

    @staticmethod
    def verify_access_token(token: str) -> Dict:
        """Verify an access token and return its payload."""
        payload = verify_token(token)
        if payload["type"] != "access":
            raise jwt.InvalidTokenError("Not an access token")
        return payload

    @staticmethod
    def verify_refresh_token(token: str) -> Dict:
        """Verify a refresh token and return its payload."""
        payload = verify_token(token)
        if payload["type"] != "refresh":
            raise jwt.InvalidTokenError("Not a refresh token")
        return payload
