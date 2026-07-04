# profiles/tasks/task_creating_profile:2
import logging
from threading import Thread

from celery import shared_task

from utilities.services import CustomizationSyncAsyncLoop

log = logging.getLogger(__name__)


@shared_task(
    name=f"{__name__}",
    bind=True,
    ignore_result=True,
    autoretry_for=(TimeoutError, ConnectionError, OSError),
    retry_backoff=True,
    max_retries=3,
    retry_backoff_max=15,
)
def task_of_profiles(self, *args, **kwargs) -> None:
    log_t = "[task_of_profiles]:"
    try:
        custom_loop = CustomizationSyncAsyncLoop(*args, **kwargs)
        custom_loop.get_new_function = lambda: True
        custom_loop.is_async = True
        wrapper = custom_loop.get_new_loop()
        log.info(log_t + " After opening a new loop & Before run the threading.Thread.")
        Thread(target=wrapper).start()
    except Exception as e:
        raise self.retry(exc=e, countdown=3)
