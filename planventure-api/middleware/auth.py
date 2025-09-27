from functools import wraps
import traceback
from flask import logging, request, jsonify, g
from models.user import User
from werkzeug.exceptions import Unauthorized


def require_auth(f):
    """Decorator to protect routes with JWT authentication."""

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise Unauthorized("No authorization header")

        try:
            # Extract token from Bearer scheme
            auth_type, token = auth_header.split()
            if auth_type.lower() != "bearer":
                raise Unauthorized("Invalid authorization scheme")

            # Verify token and get payload
            payload = User.verify_access_token(token)

            # Get user from database
            user = User.query.filter_by(email=payload["sub"]).first()
            if not user or not user.is_active:
                raise Unauthorized("Invalid or inactive user")

            # Store user in request context
            g.current_user = user
            return f(*args, **kwargs)

        except ValueError as e:
            stack_trace = traceback.format_exc()
            logging.error(f"Auth required error: {stack_trace}\n{stack_trace}")
            raise Unauthorized("Invalid authorization header format")
        except Exception as e:
            stack_trace = traceback.format_exc()
            logging.error(f"Auth required error: {stack_trace}\n{stack_trace}")
            raise Unauthorized(str(e))

    return decorated
