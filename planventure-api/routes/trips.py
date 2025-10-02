from flask import Blueprint, abort, g as request_context, jsonify, request
from middleware.auth import require_auth
from models import db
from models.trip import Trip
from werkzeug.exceptions import NotFound, BadRequest
from datetime import datetime
import logging

# Logger for trip route errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

trips_bp = Blueprint("trips", __name__)


@trips_bp.route("/trips", methods=["GET"])
@require_auth
def get_trips():
    """
    Get all trips for the current user.

    Args:
        None

    Returns:
        Response: JSON response with a list of trips of the current user.
    """
    current_user = request_context.current_user
    response = Trip.query.filter_by(user_id=current_user.id).all()
    trips = []
    for trip in response:
        try:
            trips.append(trip.to_dict())
        except Exception as e:
            # Log the error and skip the invalid trip entry
            logger.error(f"Error loading trip ID {trip.id}: {e}")
            continue
    return jsonify({"trips": trips})


@trips_bp.route("/trips/<int:trip_id>", methods=["GET"])
@require_auth
def get_trip(trip_id):
    """
    Get a specific trip by ID.

    Args:
        trip_id (int): The ID of the trip to retrieve.

    Returns:
        Response: JSON response with the trip details.

    Raises:
        NotFound: If the trip does not exist or does not belong to the current user.
    """
    trip = Trip.query.filter_by(
        id=trip_id, user_id=request_context.current_user.id
    ).first()
    if not trip:
        raise NotFound("Trip not found")
    return jsonify(trip.to_dict())


@trips_bp.route("/trips", methods=["POST"])
@require_auth
def create_trip():
    """
    Create a new trip.

    At a minimum, 'title', 'start_date', and 'end_date' must be provided in the
    request JSON.

    Args:
        title (str): Title of the trip.
        start_date (str): Start date of the trip in ISO format.
        end_date (str): End date of the trip in ISO format.
        description (str, optional): Description of the trip.

    Returns:
        Response: JSON response with the created trip details

    Raises:
        BadRequest: If required fields are missing or data is invalid.
    """
    data = request.get_json()

    required_fields = ["title", "start_date", "end_date"]

    try:
        if not all(field in data for field in required_fields):
            raise BadRequest("Missing required fields")

        trip = Trip(
            title=data["title"],
            description=data.get("description", ""),
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            user_id=request_context.current_user.id,
        )
        db.session.add(trip)
        db.session.commit()
        return jsonify(trip.to_dict()), 201
    except ValueError as e:
        raise BadRequest(str(e))


@trips_bp.route("/trips/<int:trip_id>", methods=["PUT"])
@require_auth
def update_trip(trip_id):
    """
    Updates an existing trip. The trip must belong to the current user and its trip_id
    must be provided in the URL. At least one of the fields (title, start_date, end_date,
    description) must be provided in the request JSON.

    Args:
        trip_id (int): The ID of the trip to update.
        title (str, optional): New title of the trip.
        start_date (str, optional): New start date of the trip in ISO format.
        end_date (str, optional): New end date of the trip in ISO format.
        description (str, optional): New description of the trip.

    Returns:
        Response: JSON response with the updated trip details or, if not found, a 404
        error, or if invalid data, a 400 error.

    Raises:
        NotFound: If the trip does not exist or does not belong to the current user.
    """
    trip = Trip.query.filter_by(
        id=trip_id, user_id=request_context.current_user.id
    ).first()

    try:
        if not trip:
            raise NotFound("Trip not found")

        data = request.get_json()
        if "title" in data:
            trip.title = data["title"]
        if "description" in data:
            trip.description = data["description"]
        if "start_date" in data:
            trip.start_date = data["start_date"]
        if "end_date" in data:
            trip.end_date = data["end_date"]

        db.session.commit()
        return jsonify(trip.to_dict()), 200
    except ValueError as e:
        raise BadRequest(str(e))


@trips_bp.route("/trips/<int:trip_id>", methods=["DELETE"])
@require_auth
def delete_trip(trip_id):
    """
    Delete a trip.

    Args:
        trip_id (int): The ID of the trip to delete.

    Returns:
        Response: JSON response with a success message

    Raises:
        NotFound: If the trip does not exist or does not belong to the current user.
    """
    trip = Trip.query.filter_by(
        id=trip_id, user_id=request_context.current_user.id
    ).first()
    if not trip:
        raise NotFound("Trip not found")

    db.session.delete(trip)
    db.session.commit()
    return jsonify({"message": "Trip deleted successfully"}), 204


# Error handlers
@trips_bp.errorhandler(NotFound)
def handle_not_found(e):
    """Handler for NotFound errors on trips blueprint."""
    logger.error(f"NotFound error: {e}")
    return jsonify({"error": str(e)}), 404


@trips_bp.errorhandler(BadRequest)
def handle_bad_request(e):
    """Handler for BadRequest errors on trips blueprint."""
    logger.error(f"BadRequest error: {e}")
    return jsonify({"error": str(e)}), 400
