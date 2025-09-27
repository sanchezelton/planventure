from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from models import db

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///planventure.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

# Configure JWT settings
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", app.config["SECRET_KEY"])
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    minutes=int(os.getenv("JWT_ACCESS_TOKEN_MINUTES", 30))
)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
    days=int(os.getenv("JWT_REFRESH_TOKEN_DAYS", 30))
)
app.config["JWT_ALGORITHM"] = os.getenv("JWT_ALGORITHM", "HS256")

# Configure CORS
CORS(
    app,
    resources={
        r"/*": {
            "origins": os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)

# Initialize SQLAlchemy
db.init_app(app)


@app.route("/")
def home():
    """Home route"""
    return jsonify({"message": "Welcome to PlanVenture API"})


@app.route("/health")
def health_check():
    """Health check route"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
