import os

import dotenv

# from pathlib import Path


# from persons.apps import BASE_DIR

dotenv.load_dotenv()


# DJANGO_SETTINGS_MODULE = os.getenv("DJANGO_SETTINGS_MODULE","project.settings")
DJANGO_ENV = os.getenv("DJANGO_ENV", "development")

# APP
APP_NAME = os.getenv("APP_NAME", "BookShop")
APP_PROTOCOL = os.getenv("APP_PROTOCOL", "http")
APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT = os.getenv("APP_PORT", "8003")
APP_TIME_ZONE = os.getenv("APP_TIME_ZONE", "Asia/Krasnoyarsk")
APP_MINIMUM_PASSWORD_LENGTH = int(os.getenv("APP_MINIMUM_PASSWORD_LENGTH", "7"))
APP_MAX_PASSWORD_LENGTH = int(os.getenv("APP_MAX_PASSWORD_LENGTH", "255"))
APP_BASIS_URL = (
    f"{APP_PROTOCOL}://" + f"{APP_HOST}:{APP_PORT}" if APP_PORT else f"{APP_HOST}"
)

# DATABASE EXTERNAL
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "<PASSWORD>")
POSTGRES_DB = os.getenv("POSTGRES_DB", "<DATABASE_NAME>")

JWT_ACCESS_TOKEN_LIFETIME_MINUTES = os.getenv("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", "0")
JWT_REFRESH_TOKEN_LIFETIME_DAYS = os.getenv("JWT_REFRESH_TOKEN_LIFETIME_DAYS", "0")


# USer Email
USER_EMAIL_BASIS_MESSAGE = os.getenv(
    "USER_EMAIL_BASIS_MESSAGE", "Check the your email and follow the link"
)

APP_EMAIL_HOST = os.getenv("APP_EMAIL_HOST", "mail.ru")
APP_DEFAULT_FROM_EMAIL = os.getenv("APP_DEFAULT_FROM_EMAIL", None)
APP_EMAIL_HOST_PASSWORD = os.getenv("APP_EMAIL_HOST_PASSWORD", None)

# Redis
REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "Not_password")
REDIS_DB: int = int(os.getenv("REDIS_DB", "1"))
REDIS_HOST: str = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT: str = os.getenv("REDIS_PORT", "6379")
REDIS_URL: str = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")
REDIS_MASTER_NAME: str = os.getenv("REDIS_MASTER_NAME", "master")

# Celery + Redis
# REDIS_MASTER_NAME = os.getenv("REDIS_MASTER_NAME", "root")
# REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "123")
CELERY_BROKER_URL = REDIS_URL + "/" + str(REDIS_DB)
CELERY_RESULT_BACKEND = REDIS_URL + "/" + str(REDIS_DB)

HEADLESS_MODE: bool = bool(os.getenv("HEADLESS_MODE", "False"))
