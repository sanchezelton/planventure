# Import sys module for modifying Python's runtime environment
import sys

# Import os module for interacting with the operating system
import os

# Import datetime for validating dates and times
from datetime import datetime

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from models.user import User


def test_user_creation():
    """Test creating a new user."""
    user = User(email="test@example.com", password="password123")
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert user.password_hash != "password123"  # Password should be hashed


def test_user_authentication():
    """Test user authentication."""
    user = User(email="test@example.com", password="password123")
    assert user.authenticate("password123") is True
    assert user.authenticate("wrongpassword") is False


def test_user_attributes():
    """Test user attributes."""
    user = User(email="test@example.com", password="password123")
    assert hasattr(user, "id")
    assert hasattr(user, "email")
    assert hasattr(user, "password_hash")
    assert hasattr(user, "is_active")
    assert hasattr(user, "created_at")
    assert hasattr(user, "updated_at")
