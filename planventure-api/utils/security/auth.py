from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def auth_required(fn):
    """Decorator to protect routes with JWT authentication."""

    @wraps(fn)
    def decorated(*args, **kwargs):
        """Verify JWT in request and call the decorated function."""
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({"msg": "Missing or invalid token", "error": str(e)}), 401

    return decorated


def get_current_user_id():
    """Get the user ID from the JWT token. Assumes the identity is the user ID."""
    return get_jwt_identity
