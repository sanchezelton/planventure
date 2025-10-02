from functools import wraps
import traceback
from flask import logging, request, g as request_context
from models.user import User
from werkzeug.exceptions import Unauthorized, BadRequest, NotFound
import logging

# Logger for authentication errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
            request_context.current_user = user
            return f(*args, **kwargs)

        except ValueError as e:
            logger.exception("Auth required error")
            raise Unauthorized("Invalid authorization header format")
        except Exception as e:
            exceptionList = [NotFound, Unauthorized, BadRequest]
            for item in exceptionList:
                if isinstance(e, item):
                    raise e  # Re-raise known exceptions so app or blueprint handlers can catch them
            # Log unexpected errors
            logger.exception("Auth failure")

    return decorated
