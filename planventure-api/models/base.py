from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_mixins import AllFeaturesMixin

db = SQLAlchemy()

AllFeaturesMixin.session = db.session


class BaseModel(db.Model, AllFeaturesMixin):
    """Base model with common attributes."""

    __abstract__ = True
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    def __init__(self):
        """Initialize the base model with timestamps."""
        super().__init__()
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = None

    def to_dict(self, exclude=None):
        """Convert model instance to dictionary, including datetime formatting. Overrides the method from AllFeaturesMixin."""
        if exclude is None:
            exclude = set()

        data = super().to_dict(exclude=exclude)
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data


BaseModel.set_session(db.session)
