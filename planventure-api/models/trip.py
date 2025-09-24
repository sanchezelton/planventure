from .base import BaseModel, db
from datetime import datetime, timezone


class Trip(BaseModel):
    """Trip model representing a travel plan."""

    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    itinerary = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationship
    user = db.relationship("User", back_populates="trips")

    def __repr__(self):
        return f"<Trip {self.destination}>"

    def __init__(
        self,
        title,
        user_id,
        start_date,
        end_date,
        latitude=None,
        longitude=None,
        itinerary=None,
        destination=None,
        description=None,
    ):
        """Initialize a Trip instance with validation."""
        if start_date >= end_date:
            raise ValueError("start_date must be before end_date")
        if latitude is not None and (latitude < -90 or latitude > 90):
            raise ValueError("latitude must be between -90 and 90")
        if longitude is not None and (longitude < -180 or longitude > 180):
            raise ValueError("longitude must be between -180 and 180")
        self.title = title
        self.description = description
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date
        self.latitude = latitude
        self.longitude = longitude
        self.itinerary = itinerary or {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
