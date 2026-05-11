"""
persons/tasks/tasks_celery/task_for_service_registration.py:1
"""

import logging

log = logging.getLogger(__name__)


def task_letter_send_in_email_for_registration(user_id: str) -> None:
    try:
        pass
    except Exception as e:
        log.error(e)
    finally:
        pass
