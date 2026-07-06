# persons/tasks/tasks_celery/task_create_position/__init__.py:1
import logging
from threading import Thread

from celery import shared_task

from persons.tasks.tasks_celery.task_create_position.create_position import create_position_for_EmailConfiguration
from utilities.services import CustomizationSyncAsyncLoop

log = logging.getLogger(__name__)


@shared_task(
    name="task_create_position_for_EmailConfiguration",
    bind=True,
    ignore_result=True,
    authretry_for=(TimeoutError, ConnectionError, OSError),
    retry_backoff=True,
    ratry_backoff_max=3,
    max_retries=3,
)
def task_create_position_for_EmailConfiguration(self, *args, **kwargs):
    log_t = "[task_create_position_for_EmailConfiguration]:"
    try:
        custom_loop = CustomizationSyncAsyncLoop(*args, **kwargs)
        custom_loop.get_new_function = create_position_for_EmailConfiguration
        wrapper = custom_loop.get_new_loop()
        Thread(target=wrapper).start()
    except Exception as e:
        log.warning(log_t + e.args[0] if e.args else str(e))
        raise self.retry(exc=e, max_retries=3)
