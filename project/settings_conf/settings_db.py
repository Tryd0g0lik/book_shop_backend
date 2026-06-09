import logging
import os
from pathlib import Path

from persons.apps import DEBUG
from project import BASE_DIR

# from logs import configure_logging
from project.settings_conf.settings_env import (
    APP_HOST,
    DJANGO_ENV,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from project.settings_conf.settings_security import CORS_ALLOWED_ORIGINS

# configure_logging(logging.INFO)
log = logging.getLogger(__name__)
ALLOWED_HOSTS = []
# SECURITY WARNING: don't run with debug turned on in production!

print(f"DEBUG: {DEBUG}, DJANGO_ENV: {DJANGO_ENV}")


# ============================================
# HOST
# ============================================
def get_allowed_hosts(allowed_hosts: str):
    """
    The function is for the securite connection to the allowed hosts
    """
    from django.core.exceptions import ImproperlyConfigured

    hosts = allowed_hosts.split(", ")
    hosts = [h.strip() for h in hosts if h.strip()]

    if DJANGO_ENV == "production":
        hosts.insert(0, f"{APP_HOST}")
        hosts += [
            "172.19.0.2",
            "db",
            "backend",
            "nginx",
            "celery",
            "celery_beat",
            "redis",
            "[::1]",
        ]

    if not hosts and DJANGO_ENV == "production":
        text_e = (
            "[%s]: ALLOWED_HOSTS must be set in production" % get_allowed_hosts.__name__
        )
        log.error(text_e)
        raise ImproperlyConfigured(text_e)
    # The additional merged to an IP numbers for the Docker
    # IP of Docker is dynamic
    for third in range(16, 20):  # 172.16.0.0 - 172.19.255.255
        for fourth in range(0, 256):
            hosts.append(f"172.{third}.{fourth}")
    return hosts


# ============================================
# DATABASE
# ============================================
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
ALLOWED_HOSTS += get_allowed_hosts("127.0.0.1, localhost, 0.0.0.0")

# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
if DJANGO_ENV == "testing":
    log.info(f"DJANGO_ENV == 'testing'': {DJANGO_ENV == "testing"}")
    CORS_ALLOWED_ORIGINS += [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]
    # ============================================
    # TESTING
    # ============================================
    if DEBUG:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / f"test_{(lambda: POSTGRES_DB)()}.sqlite3",
            }
        }
        log.info("SQLIte database was launched.")
    elif not DEBUG:

        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.getenv("POSTGRES_DB", "test_myapp_db"),
                "USER": os.getenv("POSTGRES_USER", "test_user"),
                "PASSWORD": os.getenv("POSTGRES_PASSWORD", "test_password"),
                "HOST": f"{(lambda: POSTGRES_HOST)()}",
                "PORT": f"{(lambda: POSTGRES_PORT)()}",
                "KEY_PREFIX": "drive_test_",  # it's my prefix for the keys
            }
        }
        log.info("Postgres database was launched.")
elif DEBUG:
    # ============================================
    # DEVELOPMENT
    # ============================================
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / f"{(lambda: POSTGRES_DB)()}.sqlite3",
        }
    }
    log.info("Sqlite database was launched.")
else:
    CORS_ALLOWED_ORIGINS += [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]
    # ============================================
    # PRODUCTION
    # ============================================
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": f"{(lambda: POSTGRES_DB)()}",
            "USER": f"{(lambda: POSTGRES_USER)()}",
            "PASSWORD": f"{(lambda: POSTGRES_PASSWORD)()}",
            "HOST": f"{(lambda: POSTGRES_HOST)()}",
            "PORT": f"{(lambda: POSTGRES_PORT)()}",
            "KEY_PREFIX": "drive_",
            "OPTIONS": {
                "connect_timeout": 30,
            },
        }
    }
    log.info("Postgres database was launched.")
