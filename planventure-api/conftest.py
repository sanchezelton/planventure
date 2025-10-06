import pytest
from app import app, db


@pytest.fixture(scope="session")
def app_instance():
    """Create and configure a new app instance for each test session."""
    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def db_instance(app_instance):
    """Create the database and tables, then drop them during cleanup"""
    db.create_all()
    yield db
    db.session.close()
    db.drop_all()


@pytest.fixture
def client(app_instance):
    """A test client for the app."""
    with app_instance.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def test_user_login_data():
    """Test user login email and password fixture."""
    return {"email": "test@example.com", "password": "securepassword123"}


@pytest.fixture
def invalid_email_data():
    """Test data with invalid email format."""
    return {
        "email": "invalid.email",  # Invalid email format
        "password": "securepassword123",
    }
