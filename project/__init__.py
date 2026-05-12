# project/__init__.py
from pathlib import Path

from .celery import celery_app as celery_app

BASE_DIR = Path(__file__).resolve().parent.parent

__all__ = ("celery_app",)
