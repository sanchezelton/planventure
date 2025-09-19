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


def test_email_validation():
    """Test email validation method."""
    # Valid email cases
    assert User.validate_email("test@example.com") is True
    assert User.validate_email("user.name+tag@domain.co.uk") is True
    assert User.validate_email("first.last+seq@domain.io") is True

    # Invalid email cases
    assert User.validate_email("invalid.email") is False
    assert User.validate_email("@domain.com") is False
    assert User.validate_email("user@.com") is False


def test_invalid_email_user_creation():
    """Test creating a user with an invalid email raises ValueError."""
    with pytest.raises(ValueError):
        User(email="invalid.email", password="password123")
