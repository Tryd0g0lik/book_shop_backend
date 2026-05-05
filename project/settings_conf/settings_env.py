import os
from pathlib import Path

import dotenv

dotenv.load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY_DJ = os.getenv("SECRET_KEY_DJ", "fr4d6650h0_d")
IS_DEBUG = os.getenv("IS_DEBUG", "1")
DEBUG = True if int(IS_DEBUG) == 1 else False
DJANGO_ENV = os.getenv("DJANGO_ENV", "development")

# APP
APP_PROTOCOL = os.getenv("APP_PROTOCOL", "http")
APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT = os.getenv("APP_PORT", "8003")
APP_TIME_ZONE = os.getenv("APP_TIME_ZONE", "Asia/Krasnoyarsk")

# DATABASE EXTERNAL
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "<PASSWORD>")
POSTGRES_DB = os.getenv("POSTGRES_DB", "<DATABASE_NAME>")

JWT_ACCESS_TOKEN_LIFETIME_MINUTES = os.getenv("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", "0")
JWT_REFRESH_TOKEN_LIFETIME_DAYS = os.getenv("JWT_REFRESH_TOKEN_LIFETIME_DAYS", "0")


CATEGORY_STATUS = [
    ("BASE", "Base"),
    ("ADMIN", "Admin"),
    ("MANAGER", "Manager"),
    ("CLIENT", "Client"),
]

# USer Email
USER_EMAIL_BASIS_MASSAGE = os.getenv(
    "USER_EMAIL_BASIS_MASSAGE", "Check the your email and follow the link"
)
