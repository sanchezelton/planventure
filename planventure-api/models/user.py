import bcrypt
from .base import BaseModel, db
from datetime import datetime


class User(BaseModel):
    """User model for authentication and user management."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Add relationship
    trips = db.relationship("Trip", back_populates="user", lazy="dynamic")

    def __repr__(self):
        """Returns a string representation of the User object."""
        return f"<User {self.email}>"

    def __init__(self, email, password):
        """Initializes a User instance with email and hashed password."""
        super().__init__()
        self.email = email
        self.set_password(password)
        self.is_active = True

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def authenticate(self, plaintext_password):
        """Verifies the plaintext password against the stored hash."""
        return bcrypt.checkpw(
            plaintext_password.encode("utf-8"), self.password_hash.encode("utf-8")
        )
