import os
from datetime import timedelta

BASE_DIR = os.path.abspath(
    os.path.dirname(os.path.dirname(__file__))
)


class Config:

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:Sakshi@123@127.0.0.1:3306/welfarebridge09"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Aiven MySQL requires SSL
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {
                "ca": os.path.join(BASE_DIR, "ca.pem")
            }
        }
    }

    # JWT
    JWT_SECRET_KEY = os.environ.get(
        "JWT_SECRET_KEY",
        "welfarebridge-super-secret-signing-key-change-this-in-production"
    )

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # CORS
    FRONTEND_ORIGIN = os.environ.get(
        "FRONTEND_ORIGIN",
        "*"
    )

    CORS_ORIGINS = "*"