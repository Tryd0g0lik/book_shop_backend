import logging

from logs import configure_logging

from .celery import celery_deribit

configure_logging(logging.INFO)
__all__ = ("celery_deribit",)
