import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    # Reads from a .env file if present (see .env.example). Falls back to a default
    # local MySQL connection if DATABASE_URL isn't set at all.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:Sakshi@123@127.0.0.1:3306/welfarebridge09"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get(
        "JWT_SECRET_KEY",
        "welfarebridge-super-secret-signing-key-change-this-in-production"
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # CORS: wildcard is safe here because auth uses a JWT in the Authorization header
    # (not cookies), so there's no CSRF risk from allowing any origin. This also means
    # it doesn't matter whether you open the frontend via a local server or by double
    # clicking the HTML files directly (file:// origin).
    FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "*")
    CORS_ORIGINS = "*"
