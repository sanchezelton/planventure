# Borrowed and adapted from: https://www.digitalocean.com/community/tutorials/unit-test-in-flask
# Import sys module for modifying Python's runtime environment
import sys

# Import os module for interacting with the operating system
import os

# Import datetime for validating dates and times
from datetime import datetime

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app instance from the main app file
from app import app

# Import pytest for writing and running tests
import pytest
from models import db
from models.user import User


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_user_data():
    """Test user data fixture."""
    return {"email": "test@example.com", "password": "securepassword123"}


@pytest.fixture
def invalid_email_data():
    """Test data with invalid email format."""
    return {
        "email": "invalid.email",  # Invalid email format
        "password": "securepassword123",
    }


def test_home(client):
    """Test the root/home route."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to PlanVenture API"}


def test_health(client):
    """Test the health route."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert datetime.strptime(response.json["timestamp"], "%Y-%m-%dT%H:%M:%S.%f")


def test_non_existent_route(client):
    """Test for a non-existent route."""
    response = client.get("/non-existent")
    assert response.status_code == 404


def test_user_registration(client, test_user_data):
    """Test user registration endpoint."""
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 201
    assert "access_token" in response.json
    assert "refresh_token" in response.json
    assert response.json["message"] == "User registered successfully"


def test_duplicate_registration(client, test_user_data):
    """Test registration with existing email."""
    # First registration
    client.post("/auth/register", json=test_user_data)

    # Attempt duplicate registration
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 409
    assert "error" in response.json
    assert "already registered" in response.json["error"].lower()


def test_user_login(client, test_user_data):
    """Test user login endpoint."""
    # Register user first
    client.post("/auth/register", json=test_user_data)

    # Test login
    response = client.post("/auth/login", json=test_user_data)
    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json
    assert response.json["message"] == "Login successful"


def test_invalid_login(client, test_user_data):
    """Test login with invalid credentials."""
    # Register user first
    client.post("/auth/register", json=test_user_data)

    # Test with wrong password
    invalid_data = test_user_data.copy()
    invalid_data["password"] = "wrongpassword"
    response = client.post("/auth/login", json=invalid_data)
    assert response.status_code == 401
    assert "error" in response.json


def test_token_refresh(client, test_user_data):
    """Test token refresh endpoint."""
    # Register and login user first
    client.post("/auth/register", json=test_user_data)
    login_response = client.post("/auth/login", json=test_user_data)

    # Test token refresh
    refresh_token = login_response.json["refresh_token"]
    response = client.post(
        "/auth/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_register_invalid_email(client, invalid_email_data):
    """Test registration with invalid email format."""
    response = client.post("/auth/register", json=invalid_email_data)
    assert response.status_code == 400
    assert "error" in response.json
    assert "invalid email format" in response.json["error"].lower()
