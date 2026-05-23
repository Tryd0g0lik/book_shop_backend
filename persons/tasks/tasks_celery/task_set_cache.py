"""
persons/tasks/tasks_celery/task_cache_user_email_before_verification.py:1
"""

import json
import logging
import time
from threading import Thread
from uuid import uuid4

from celery import shared_task

# from django.core.mail import send_mail
from redis import ConnectionError, TimeoutError

from persons.services import CustomizationSyncAsyncLoop

log = logging.getLogger(__name__)
task_id = uuid4()


async def cache_user_data(*args, **kwargs) -> bool:
    """
    :param list or tuple args: This is argument a key of cache.
    :param dict kwargs: This is argument a value of cache.
    :return: void
    """
    import asyncio

    from persons import EnumTemplatesREGEX
    from persons.apps import cachemanager

    PERSON_KEYS_OF_CACHE_IN_REGEX = (
        EnumTemplatesREGEX.PERSON_KEYS_OF_CACHE_IN_REGEX.value
    )
    log_t = "[task cache_user_data]:"
    k = args[0]
    log.info(
        log_t + f"TEST DEBUG k: {str(k)} & args: {str(args)} & kwargs: {str(kwargs)} "
    )
    if not PERSON_KEYS_OF_CACHE_IN_REGEX.search(k):
        log.error(
            " ".join(
                [
                    log_t[:-1],
                    "[child_process]:",
                    "Attribute 'args' is invalid",
                ]
            )
        )

        return False

    task = asyncio.create_task(
        cachemanager.asave(
            key=str(k),
            ttl=300,
            default=kwargs,
            # default=json.dumps(kwargs, ensure_ascii=False).encode("utf-8"),
        )
    )
    try:
        await asyncio.wait_for(task, timeout=60)
        return True
    except asyncio.TimeoutError as e:
        log.warning(
            " ".join(
                [
                    log_t[:-1],
                    "[child_process]:",
                    " Cache user data timed out. TimeoutError: " + str(e),
                ]
            )
        )
        try:
            await task
        except asyncio.CancelledError as e:
            log.warning(
                " ".join(
                    [
                        log_t[:-1],
                        "[child_process]:",
                        "Cache user data Cancelled CancelledError: " + str(e),
                    ]
                )
            )
            task.cancel()
    except Exception as e:
        log.error(
            " ".join(
                [
                    log_t[:-1],
                    "[child_process]:",
                    "Cache user data Cancelled Error: " + str(e),
                ]
            )
        )
        task.cancel()
    return False


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
    log_t = "[task_of_cache]:"
    args_len = len(args)
    kwargs_len = len(kwargs) if kwargs is not None else 0
    if args_len > 0 and kwargs_len > 0:
        custom_loop = CustomizationSyncAsyncLoop(*args, **kwargs)
        custom_loop.get_new_function = cache_user_data
        custom_loop.is_async = True
        wrapper = custom_loop.get_new_loop()
        log.info(
            log_t + " After opening a new loop. & Before run the threading.Thread."
        )
        Thread(target=wrapper).start()
    else:
        time.sleep(3)
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
