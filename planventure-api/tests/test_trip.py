import pytest
from datetime import datetime, timedelta, timezone
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


def test_trip_timezone_handling(sample_user):
    """Test that Trip handles timezone-aware dates correctly."""
    # Create dates in different timezones
    utc_start = datetime.now(timezone.utc)
    utc_end = utc_start + timedelta(days=5)

    # Create trip with UTC dates
    utc_trip = Trip(
        title="UTC Trip",
        description="A trip with UTC dates",
        start_date=utc_start,
        end_date=utc_end,
        user_id=sample_user.id,
    )

    # Test timezone awareness is preserved
    assert utc_trip.start_date.tzinfo is not None
    assert utc_trip.end_date.tzinfo is not None

    # Test with different timezone (EST)
    est_tz = timezone(timedelta(hours=-5))
    est_start = utc_start.astimezone(est_tz)
    est_end = utc_end.astimezone(est_tz)

    # Create trip with EST dates
    est_trip = Trip(
        title="EST Trip",
        description="A trip with EST dates",
        start_date=est_start,
        end_date=est_end,
        user_id=sample_user.id,
    )

    # Verify that dates are equivalent regardless of timezone
    assert est_trip.start_date == utc_trip.start_date
    assert est_trip.end_date == utc_trip.end_date

    # Verify date comparisons work across timezones
    assert est_trip.start_date < est_trip.end_date
    assert utc_trip.start_date < utc_trip.end_date
    assert est_trip.start_date.timestamp() == utc_trip.start_date.timestamp()


def test_trip_timezone_edge_case(sample_user):
    """Test that Trip validation catches timezone edge cases where dates appear equal but aren't."""
    # Create a base time
    base_time = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)

    # Create timezones 12 hours apart
    tz_west = timezone(timedelta(hours=-6))  # UTC-6
    tz_east = timezone(timedelta(hours=6))  # UTC+6

    # When it's 12:00 in UTC-6, it's already 00:00 next day in UTC+6
    start_date = base_time.astimezone(tz_west)  # Shows as 06:00 UTC-6
    end_date = base_time.astimezone(tz_east)  # Shows as 18:00 UTC+6

    # This should raise ValueError because the dates are actually different
    # despite showing the same hour in their respective timezones
    with pytest.raises(ValueError, match="start_date must be before end_date"):
        Trip(
            title="Timezone Edge Case Trip",
            description="A trip with tricky timezone dates",
            start_date=start_date,
            end_date=end_date,
            user_id=sample_user.id,
        )
