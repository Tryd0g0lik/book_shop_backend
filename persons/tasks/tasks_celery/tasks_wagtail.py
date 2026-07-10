# persons/tasks/tasks_celery/task_create_position_wagtail_first_login.py:1

import logging

from celery import shared_task

from persons.tasks.tasks_celery.task_create_position.create_position_wagtail_profile import (
    create_some_position_at_wagtail_profile,
)

log = logging.getLogger(__name__)


@shared_task(
    name="task_get_send_letter",
    bind=True,
    ignore_result=True,
    autoretry_for=(TimeoutError, ConnectionError, OSError),
    retry_backoff=True,
    max_retries=3,
    retry_backoff_max=30,
)
def tasks_position_wagtail(self, *args, **kwargs) -> None:
    from threading import Thread

    from utilities.services import CustomizationSyncAsyncLoop

    log_t = "[tasks_position_wagtail]:"
    try:
        custom_loop = CustomizationSyncAsyncLoop(*args, **kwargs)
        custom_loop.get_new_function = create_some_position_at_wagtail_profile
        wrapper = custom_loop.get_new_loop()
        log.info(
            log_t + " After opening a new loop. & Before run the threading.Thread."
        )
        Thread(target=wrapper).start()
    except Exception as e:
        log.info(log_t + str(e))
        raise self.retry(exc=e, countdown=30)
