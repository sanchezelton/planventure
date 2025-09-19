import pytest
from datetime import datetime, timedelta
from models.trip import Trip
from models.user import User


@pytest.fixture
def sample_user():
    """Test fixture for creating a sample user."""
    return User(email="test@example.com", password="password123")


@pytest.fixture
def sample_trip(sample_user):
    """Test fixture for creating a sample trip."""
    return Trip(
        title="Test Trip",
        description="A test trip",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=5),
        user_id=sample_user.id,
    )


def test_trip_creation(sample_trip):
    """Test creating a Trip instance."""
    assert sample_trip.title == "Test Trip"
    assert sample_trip.description == "A test trip"
    assert isinstance(sample_trip.start_date, datetime)
    assert isinstance(sample_trip.end_date, datetime)


def test_trip_dates_validation(sample_user):
    """Test that Trip raises ValueError if end_date is before start_date."""
    with pytest.raises(ValueError):
        Trip(
            title="Invalid Trip",
            description="Trip with invalid dates",
            start_date=datetime.now()
            + timedelta(days=5),  # start_date is after end_date
            end_date=datetime.now(),  # end_date is before start_date
            user_id=sample_user.id,
        )


def test_trip_coordinates_validation(sample_user):
    """Test that Trip raises ValueError if latitude or longitude fall out of bounds."""
    with pytest.raises(ValueError):
        Trip(
            title="Invalid Trip",
            description="Trip with invalid coordinates",
            start_date=datetime.now() + timedelta(days=5),
            end_date=datetime.now(),
            user_id=sample_user.id,
            latitude=100,  # Invalid latitude
        )
    with pytest.raises(ValueError):
        Trip(
            title="Invalid Trip",
            description="Trip with invalid coordinates",
            start_date=datetime.now() + timedelta(days=5),
            end_date=datetime.now(),
            user_id=sample_user.id,
            longitude=200,  # Invalid longitude
        )
    with pytest.raises(ValueError):
        Trip(
            title="Invalid Trip",
            description="Trip with invalid coordinates",
            start_date=datetime.now() + timedelta(days=5),
            end_date=datetime.now(),
            user_id=sample_user.id,
            latitude=-100,  # Invalid latitude
            longitude=200,  # Invalid longitude
        )


def test_trip_attributes(sample_trip):
    """Test that Trip has all required attributes."""
    assert hasattr(sample_trip, "id")
    assert hasattr(sample_trip, "title")
    assert hasattr(sample_trip, "description")
    assert hasattr(sample_trip, "start_date")
    assert hasattr(sample_trip, "end_date")
    assert hasattr(sample_trip, "user_id")
    assert hasattr(sample_trip, "created_at")
    assert hasattr(sample_trip, "updated_at")
    assert hasattr(sample_trip, "latitude")  # New attribute
    assert hasattr(sample_trip, "longitude")  # New attribute


def test_trip_user_relationship(sample_trip, sample_user):
    """Test the relationship between Trip and User."""
    assert sample_trip.user_id == sample_user.id
