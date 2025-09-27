from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base model with common attributes."""

    __abstract__ = True
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    def __init__(self):
        super().__init__()
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = None
