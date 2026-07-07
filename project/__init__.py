# project/__init__.py
from pathlib import Path
from typing import Optional

from django.core.exceptions import ImproperlyConfigured

from .celery import celery_app as celery_app

BASE_DIR = Path(__file__).resolve().parent.parent

__all__ = ("celery_app", "AbstractError")


class AbstractError(ImproperlyConfigured):
    def __init__(self, log_message: Optional[str] = "We do not have the valid data!"):
        self._log_message = log_message
        message: str = f"[{self.__class__.__name__}]:"

        if log_message:
            message += f"\n{message}" + self._log_message
        super().__init__(message)

    @property
    def _log_message(self):
        return self.__message

    @_log_message.setter
    def _log_message(self, log_message: Optional[str] = None):
        self.__message: Optional[str] = log_message
