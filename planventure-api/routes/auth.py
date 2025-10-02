import logging
import traceback
from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized
import re

auth_bp = Blueprint("auth", __name__)  # Blueprint for authentication routes

# Logger for authentication errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InvalidCredentials(Unauthorized):
    """Exception for invalid login credentials."""

    description = "Invalid email or password"


@auth_bp.route("/register", methods=["POST"])
def post_register():
    """Registers a new user with email validation.

    Args:
        email (str): The new user's email address
        password (str): The new user's password

    Returns:
        Response: A 201 successful HTTP status response with tokens or
        errors with a...
        • 400 error message if the request is invalid
        • 409 error message if the email is already registered.
        • 500 error message if registration fails for some other reason.
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not all(k in data for k in ["email", "password"]):
            return jsonify({"error": "Email and password are required"}), 400

        # Validate email format
        if not User.validate_email(data["email"]):
            return jsonify({"error": "Invalid email format"}), 400

        # Check if user already exists
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already registered"}), 409

        # Create new user
        user = User(email=data["email"], password=data["password"])
        db.session.add(user)
        db.session.commit()

        # Generate tokens
        tokens = user.generate_auth_tokens()

        return (
            jsonify(
                {
                    "message": "User registered successfully",
                    **tokens,
                }
            ),
            201,
        )

    except ValueError as e:
        logger.exception("ValueError")
        return jsonify({"error": str(e)}), 400
    except Conflict as e:
        logger.exception("Conflict")
        return jsonify({"error": str(e)}), 409
    except BadRequest as e:
        logger.exception("BadRequest")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        logger.exception("Registration error")
        return jsonify({"error": f"Registration failed: {e}"}), 500


@auth_bp.route("/login", methods=["POST"])
def post_login():
    """Authenticate user and return JWT tokens.

    Args:
        email (str): The user's email address
        password (str): The user's password

    Returns:
        Response: A 200 successful HTTP status response with a successful login message
        along with tokens and a user object with the id and email address of the user.
        Otherwise, it returns errors with a...
        • 400 error message if the request is invalid
        • 401 error message if credentials are invalid or account is deactivated
        • 500 error message if login fails for some other reason."""
    try:
        data = request.get_json()

        # Validate required fields
        if not all(k in data for k in ["email", "password"]):
            raise BadRequest("Email and password are required")

        # Find user by email
        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.authenticate(data["password"]):
            raise InvalidCredentials()

        # Check if user is active
        if not user.is_active:
            raise Unauthorized("Account is deactivated")

        # Generate tokens
        tokens = user.generate_auth_tokens()

        return jsonify(
            {
                "message": "Login successful",
                "user": {"id": user.id, "email": user.email},
                **tokens,
            }
        )

    except (BadRequest, Unauthorized) as e:
        logger.exception("Login failed")
        return jsonify({"error": str(e)}), e.code
    except Exception as e:
        logger.exception("Login error")
        return jsonify({"error": f"Login failed: {e}"}), 500


@auth_bp.route("/refresh", methods=["POST"])
def refresh_token():
    """Refresh access token using refresh token.

    Args:
        None (see Headers below)

    Headers:
        Authorization (str): Bearer <refresh_token>

    Returns:
        Response: A 200 successful HTTP status response with new tokens or
        errors with a...
        • 401 error message if the token is invalid or user is inactive."""
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise Unauthorized("No authorization header")

        auth_type, token = auth_header.split()
        if auth_type.lower() != "bearer":
            raise Unauthorized("Invalid authorization scheme")

        # Verify refresh token
        payload = User.verify_refresh_token(token)

        # Get user and generate new tokens
        user = User.query.filter_by(email=payload["sub"]).first()
        if not user or not user.is_active:
            raise Unauthorized("Invalid or inactive user")

        tokens = user.generate_auth_tokens()
        return jsonify({"message": "Token refreshed successfully", **tokens})

    except Exception as e:
        logger.exception("Refresh access token error")
        return jsonify({"error": str(e)}), 401
