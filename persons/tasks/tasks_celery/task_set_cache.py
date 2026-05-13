"""
persons/tasks/tasks_celery/task_cache_user_email_before_verification.py:1
"""

import json
import logging
import time
from uuid import uuid4

from celery import shared_task
from django.core.mail import send_mail
from redis import ConnectionError, TimeoutError

from persons.services import CustomizationSyncAsyncLoop

log = logging.getLogger(__name__)
task_id = uuid4()


async def cache_user_data(*args, **kwargs) -> None:
    """
    :param list or tuple args: This is argument a key of cache.
    :param dict kwargs: This is argument a value of cache.
    :return: void
    """
    import asyncio

    log_t = "[task cache_user_data]:"

    def child_process():
        from persons.services import Cacher

        # ============================================
        # CACHE SERVER
        # ============================================
        cacher = Cacher(db=1)
        cacher.related()
        connected = cacher.connected
        # Checking of connection
        if not cacher.is_connected:
            error_t = " ".join(
                [log_t, " Connecting to the cache server has not exists."]
            )
            log.error(error_t)
            return
        # Here we make caching of data.
        # ============================================
        # SAVING DATA BEFORE REGISTRATION
        # ============================================
        try:

            with connected() as conn:
                log.info("[task cache_user_data]: Before caching the new data")
                k = args[0]
                conn.setex(
                    str(k), 300, json.dumps(kwargs, ensure_ascii=False).encode("utf-8")
                )
                log.info("[task cache_user_data]: Data was cached successfully!")

        except Exception as e:
            log.error(e)
            return

    task = asyncio.create_task(asyncio.to_thread(child_process))
    try:
        await asyncio.wait_for(task, timeout=60)
    except asyncio.TimeoutError as e:
        log.warning(log_t + " Cache user data timed out. TimeoutError: " + str(e))
        # task.cancel()
        try:
            await task
        except asyncio.CancelledError as e:
            log.warning(log_t + " Cache user data Cancelled CancelledError: " + str(e))
            task.cancel()
    except Exception as e:
        log.error(log_t + " Cache user data Cancelled Error: " + str(e))
        task.cancel()


@shared_task(
    name="task_set_cache",
    bind=True,
    ignore_result=True,
    autoretry_for=(TimeoutError, ConnectionError, OSError, Exception),
    retry_backoff=True,
    max_retries=3,
    retry_backoff_max=30,
)
def task_of_cache(self, *args, **kwargs) -> None:
    """
    This is a task, from the Celery, for caching purposes from the persons.
    :param self: This is setting from the Celery.
    :param list or tuple args: This is data for caching.
    :param dict kwargs: This is data for caching.
    :return: void
    """
    args_len = len(args)
    kwargs_len = len(kwargs) if kwargs is not None else 0
    if args_len > 0 and kwargs_len > 0:
        custom_loop = CustomizationSyncAsyncLoop(*args, **kwargs)
        custom_loop.get_new_function = cache_user_data
        wrapper = custom_loop.get_new_loop()
        wrapper()
    else:
        time.sleep(2)
    return
    # loop = asyncio.get_event_loop()
    # # run_asyncio_debug(loop)
    # try:
    #     asyncio.set_event_loop(loop)
    #     task = asyncio.to_thread(cache_user_data, *args, **kwargs)
    #     loop.run_until_complete(task)
    #
    # except Exception as e:
    #     loop.close()
    #     log.error(
    #         f"""[task_scraper_company_page]: {e.args[0] if e.args else str(e)} \n"""
    #     )
