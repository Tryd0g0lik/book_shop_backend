"""
project/celery.py:1
"""

from celery import Celery
from kombu import Exchange, Queue

from project import celeryconfig
from project.settings_conf.settings_env import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery_deribit = Celery(
    __name__,
    broker=f"{CELERY_BROKER_URL}",
    backend=f"{CELERY_RESULT_BACKEND}",
    include=[
        "persons/tasks/tasks_celery/task_for_service_registration.py",
    ],
)
celery_deribit.config_from_object(celeryconfig)

celery_deribit.conf.task_queues = (
    Queue("default", Exchange("default"), routing_key="task.#"),
    Queue("high", Exchange("high"), routing_key="high.#"),
    Queue("beat", Exchange("beat"), routing_key="beat.#"),
    Queue("low", Exchange("low"), routing_key="low.#"),
    Queue("celery"),
)
celery_deribit.conf.task_default_queue = "default"
celery_deribit.conf.task_default_exchange = "high"
celery_deribit.conf.task_default_routing_key = "task.default"

celery_deribit.conf.beat_schedule = {
    "add-every-60-seconds": {
        "task": "persons.tasks.tasks_celery.task_for_service_registration.< task name>",
        "schedule": 45,  # receiving data from the deribit server.
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
    # },
}
