import bcrypt
from typing import Tuple


def generate_salt() -> bytes:
    """Generate a random salt for password hashing."""
    return bcrypt.gensalt()


def hash_password(password: str, salt: bytes = None) -> Tuple[bytes, bytes]:
    """
    Hash a password with a salt. If no salt is provided, generate one.
    Returns a tuple of (hashed_password, salt).
    """
    if not salt:
        salt = generate_salt()

    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed, salt


def verify_password(password: str, hashed_password: bytes) -> bool:
    """
    Verify a password against its hash.
    Returns True if password matches, False otherwise.
    """
    password_bytes = password.encode("utf-8")
    try:
        return bcrypt.checkpw(password_bytes, hashed_password)
    except Exception:
        return False
