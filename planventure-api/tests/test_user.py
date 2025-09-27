# Import sys module for modifying Python's runtime environment
import sys

# Import copy for copying datetime objects
from copy import copy

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
    assert user.password_hash is not None
    assert user.password_salt is not None
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime) or user.updated_at is None


def test_password_update():
    """Test updating user password."""
    user = User(email="test@example.com", password="password123")
    original_hash = user.password_hash
    original_updated_at = user.updated_at
    assert original_updated_at is None

    # Wait a moment to ensure timestamp difference
    import time

    time.sleep(0.1)

    # Update password and check changes
    user.set_password("newpassword456")
    assert user.password_hash != original_hash
    assert user.updated_at is not None
    updated_hash = user.password_hash
    updated_updated_at = user.updated_at

    # Wait and update again to check updated_at changes
    time.sleep(0.1)
    user.set_password("newpassword789")
    assert user.password_hash != updated_hash
    assert user.updated_at is not None
    assert user.updated_at > updated_updated_at

    # Verify authentication with new and old passwords
    assert user.authenticate("newpassword789") is True
    assert user.authenticate("password123") is False


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


def test_password_related_attributes():
    """Test password-related attributes and methods."""
    user = User(email="test@example.com", password="password123")
    assert hasattr(user, "password_hash")
    assert hasattr(user, "password_salt")
    assert hasattr(user, "authenticate")
    assert hasattr(user, "set_password")


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
