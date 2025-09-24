import pytest
from utils.security import hash_password, verify_password, generate_salt


def test_password_hashing():
    """Test password hashing and verification."""
    password = "mysecretpassword123"

    # Test basic hashing
    hashed, salt = hash_password(password)
    assert hashed != password.encode("utf-8")
    assert salt is not None
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

    # Test consistency with same salt
    hashed1, salt = hash_password(password)
    hashed2, _ = hash_password(password, salt)
    assert hashed1 == hashed2

    # Test different salts produce different hashes
    hashed3, salt3 = hash_password(password)
    assert hashed1 != hashed3
    assert salt != salt3


def test_verify_password_with_invalid_hash():
    """Test password verification with invalid hash."""
    assert verify_password("password123", b"invalid_hash") is False
    assert verify_password("password123", b"") is False


def test_salt_generation():
    """Test salt generation."""
    salt1 = generate_salt()
    salt2 = generate_salt()
    assert salt1 != salt2
    assert len(salt1) > 16  # Ensure sufficient salt length
    assert isinstance(salt1, bytes)
    assert isinstance(salt2, bytes)
