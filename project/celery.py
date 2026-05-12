"""
project/celery.py:1
"""

import os
import sys
from pathlib import Path

from celery import Celery, group
from celery.schedules import crontab
from kombu import Exchange, Queue

celery_app = Celery(
    "person",
    group="signup",
    include=[
        "persons.tasks.tasks_celery.task_cache_user_email_before_verification",
    ],
)

celery_app.config_from_object("project.celeryconfig", namespace="CELERY")
# celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.conf.task_queues = (
    Queue("default", Exchange("default"), routing_key="task.#"),
    Queue("high", Exchange("high"), routing_key="high.#"),
    Queue("beat", Exchange("beat"), routing_key="beat.#"),
    Queue("low", Exchange("low"), routing_key="low.#"),
    Queue("celery"),
)
celery_app.conf.task_default_queue = "default"
celery_app.conf.task_default_exchange = "high"
celery_app.conf.task_default_routing_key = "task.default"

celery_app.conf.beat_schedule = {
    "add-every-1-seconds": {
        "task": "task_caching_before_verification",
        "options": {
            "queue": "high",
            "routing_key": "high.priority",
            "expires": 60,
        },
    },
    # "postman-every-60-seconds": {
    #     "task": "scraper.tasks.celery.task_send_every_60_seconds.task_celery_postman_currency",
    #     "schedule": crontab(minute="*/1"),  # Send data (received above ) by SSE.
    #     "options": {
    #         "queue": "default",
    #         "routing_key": "task.default",
    #         "expires": 40,
    #     },
    # "schedule": crontab(hour=1, minute=0),
    # },
}
