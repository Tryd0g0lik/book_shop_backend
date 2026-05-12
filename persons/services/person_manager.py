"""
persons/services/person_manager.py:1
"""

import logging

from persons.tasks.tasks_celery.task_cache_user_email_before_verification import (
    task_caching_before_verification,
)

log = logging.getLogger(__name__)


class PersonManager:
    def __init__(self):
        self.log_t = "[%s]:" % PersonManager.__class__.__name__

    async def send_signal(self, *args, **kwargs) -> bool:
        """
        TODO: Sending task and data to cache server.
        Here we is sending task and data. It run a task.
        :param list args: data for caching.
        :param dic kwargs:  data for caching.
        :return:
        """
        try:
            # This is task for caching data before verification.
            # Time interval is every 1 seconds
            task_caching_before_verification.apply_async(args, kwargs)
        except Exception as e:
            log.error(e)
            return False
        finally:
            pass
        return True
