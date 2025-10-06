import pytest
import json
from flask import jsonify, url_for
from datetime import datetime, timedelta, timezone
from models.trip import Trip
from models.user import User

# Import the Flask app instance from the main app file
from conftest import db_instance


@pytest.fixture(scope="session")
def in_db_sample_user(test_user_login_data, db_instance):
    """Test fixture for creating a sample user and adding to the database."""
    db_instance.session.rollback()  # Roll back any failed transactions
    db_instance.session.query(User).delete()  # Clear all users
    db_instance.session.commit()
    # create user instance and add the user to the db, then yield it
    in_user = User(**test_user_login_data)
    db_instance.session.add(in_user)
    db_instance.session.commit()
    yield {
        "user": in_user,
        "auth_headers": {
            "Authorization": f"Bearer {in_user.generate_auth_tokens()['access_token']}",
            "Content-Type": "application/json",
        },
    }
    db_instance.session.rollback()  # Roll back any failed transactions
    db_instance.session.query(User).delete()  # Clear all users
    db_instance.session.commit()


@pytest.fixture(scope="session")
def sample_trip(in_db_sample_user, db_instance):
    """Test fixture for creating a sample trip but does NOT add it to the database."""
    db_instance.session.rollback()  # Roll back any failed transactions
    db_instance.session.query(Trip).delete()  # Clear trips first
    db_instance.session.commit()

    in_user = in_db_sample_user["user"]

    # Create a new trip associated with the sample user
    trip = Trip(
        title="Test Trip",
        description="A test trip",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=5),
        user_id=in_user.id,
    )
    yield trip
    db_instance.session.rollback()  # Roll back any failed transactions
    db_instance.session.query(Trip).delete()  # Clear all users
    db_instance.session.commit()


@pytest.fixture(scope="session")
def in_db_sample_trip(sample_trip, db_instance):
    """Test fixture for creating a sample trip AND adds it to the database."""
    db_instance.session.rollback()  # Roll back any failed transactions
    db_instance.session.query(Trip).delete()  # Clear trips first
    db_instance.session.commit()

    # Create a new trip associated with the sample user
    db_instance.session.add(sample_trip)
    db_instance.session.commit()
    yield sample_trip
    db_instance.session.rollback()  # Roll back any failed transactions
    db_instance.session.query(Trip).delete()  # Clear all users
    db_instance.session.commit()


def test_trip_creation(sample_trip):
    """Test creating a Trip instance."""
    assert sample_trip.title == "Test Trip"
    assert sample_trip.description == "A test trip"
    assert isinstance(sample_trip.start_date, datetime)
    assert isinstance(sample_trip.end_date, datetime)


def test_trip_dates_validation(in_db_sample_user):
    """Test that Trip raises ValueError if end_date is before start_date."""
    in_user = in_db_sample_user["user"]
    with pytest.raises(ValueError):
        Trip(
            title="Invalid Trip",
            description="Trip with invalid dates",
            start_date=datetime.now()
            + timedelta(days=5),  # start_date is after end_date
            end_date=datetime.now(),  # end_date is before start_date
            user_id=in_user.id,
        )


def test_trip_coordinates_validation(in_db_sample_user):
    """Test that Trip raises ValueError if latitude or longitude fall out of bounds."""
    in_user = in_db_sample_user["user"]
    with pytest.raises(ValueError):
        Trip(
            title="Invalid Trip",
            description="Trip with invalid coordinates",
            start_date=datetime.now() + timedelta(days=5),
            end_date=datetime.now(),
            user_id=in_user.id,
            latitude=100,  # Invalid latitude
        )
    with pytest.raises(ValueError):
        Trip(
            title="Invalid Trip",
            description="Trip with invalid coordinates",
            start_date=datetime.now() + timedelta(days=5),
            end_date=datetime.now(),
            user_id=in_user.id,
            longitude=200,  # Invalid longitude
        )
    with pytest.raises(ValueError):
        Trip(
            title="Invalid Trip",
            description="Trip with invalid coordinates",
            start_date=datetime.now() + timedelta(days=5),
            end_date=datetime.now(),
            user_id=in_user.id,
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
    assert hasattr(sample_trip, "latitude")
    assert hasattr(sample_trip, "longitude")


def test_trip_latlong_together_validation(in_db_sample_user):
    """Test that Trip raises ValueError if only one of latitude or longitude is provided."""
    in_user = in_db_sample_user["user"]
    with pytest.raises(ValueError):
        Trip(
            title="Invalid Trip",
            description="Trip with only latitude",
            start_date=datetime.now() + timedelta(days=5),
            end_date=datetime.now(),
            user_id=in_user.id,
            latitude=45.0,  # Only latitude provided
        )
    with pytest.raises(ValueError):
        Trip(
            title="Invalid Trip",
            description="Trip with only longitude",
            start_date=datetime.now() + timedelta(days=5),
            end_date=datetime.now(),
            user_id=in_user.id,
            longitude=90.0,  # Only longitude provided
        )


def test_trip_user_relationship(sample_trip, in_db_sample_user):
    """Test the relationship between Trip and User."""
    in_user = in_db_sample_user["user"]
    assert sample_trip.user_id == in_user.id


def test_trip_timezone_handling(in_db_sample_user):
    """Test that Trip handles timezone-aware dates correctly."""
    in_user = in_db_sample_user["user"]

    # Create dates in different timezones
    utc_start = datetime.now(timezone.utc)
    utc_end = utc_start + timedelta(days=5)

    # Create trip with UTC dates
    utc_trip = Trip(
        title="UTC Trip",
        description="A trip with UTC dates",
        start_date=utc_start,
        end_date=utc_end,
        user_id=in_user.id,
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
        user_id=in_user.id,
    )

    # Verify that dates are equivalent regardless of timezone
    assert est_trip.start_date == utc_trip.start_date
    assert est_trip.end_date == utc_trip.end_date

    # Verify date comparisons work across timezones
    assert est_trip.start_date < est_trip.end_date
    assert utc_trip.start_date < utc_trip.end_date
    assert est_trip.start_date.timestamp() == utc_trip.start_date.timestamp()


def test_trip_timezone_edge_case(in_db_sample_user):
    """Test that Trip validation catches timezone edge cases where dates appear equal but aren't."""
    in_user = in_db_sample_user["user"]

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
            user_id=in_user.id,
        )


def test_get_trips(client, in_db_sample_user, in_db_sample_trip):
    """Test GET /api/trips endpoint."""
    auth_headers = in_db_sample_user["auth_headers"]

    # Make request within the same context
    response = client.get("/api/trips", headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data["trips"]) == 1
    assert data["trips"][0]["title"] == in_db_sample_trip.title


def test_get_trip_by_id(client, in_db_sample_user, in_db_sample_trip):
    """Test GET /api/trips/<id> endpoint."""
    auth_headers = in_db_sample_user["auth_headers"]
    in_user = in_db_sample_user["user"]
    response = client.get(f"/api/trips/{in_user.id}", headers=auth_headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["title"] == in_db_sample_trip.title


def test_create_trip(client, in_db_sample_user, sample_trip):
    """Test POST /api/trips endpoint."""
    auth_headers = in_db_sample_user["auth_headers"]
    # Note: sample_trip is not yet in the database
    response = client.post(
        "/api/trips",
        headers=auth_headers,
        json=sample_trip.to_dict(),
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["title"] == sample_trip.title
    assert "id" in data


def test_update_trip(client, in_db_sample_trip, in_db_sample_user):
    """Test PUT /api/trips/<id> endpoint."""
    auth_headers = in_db_sample_user["auth_headers"]

    update_data = {
        "title": "Updated Trip Title",
        "description": "Updated description",
    }

    response = client.put(
        f"/api/trips/{in_db_sample_trip.id}",
        headers=auth_headers,
        json=update_data,
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]


def test_delete_trip(client, in_db_sample_user, in_db_sample_trip):
    """Test DELETE /api/trips/<id> endpoint."""
    auth_headers = in_db_sample_user["auth_headers"]
    response = client.delete(
        f"/api/trips/{in_db_sample_trip.id}",
        headers=auth_headers,
    )
    assert response.status_code == 204

    # Verify trip was deleted using fresh auth headers
    response = client.get(f"/api/trips/{in_db_sample_trip.id}", headers=auth_headers)
    assert response.status_code == 404


def test_unauthorized_access(client, sample_trip):
    """Test accessing endpoints without authentication."""
    response = client.get("/api/trips")
    assert response.status_code == 401


def test_invalid_trip_creation(client, in_db_sample_user):
    """Test creating trip with invalid data."""
    auth_headers = in_db_sample_user["auth_headers"]
    invalid_data = {
        "title": "Invalid Trip",
        # Missing required fields
    }
    response = client.post(
        "/api/trips",
        headers=auth_headers,
        json=invalid_data,
    )
    assert response.status_code == 400
