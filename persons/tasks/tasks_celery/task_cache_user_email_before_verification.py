"""
persons/tasks/tasks_celery/task_cache_user_email_before_verification.py:1
"""

import asyncio
import json
import logging
from uuid import uuid4

from celery import shared_task
from redis import ConnectionError, TimeoutError

from persons.services import CustomizationSyncAsyncLoop

log = logging.getLogger(__name__)
task_id = uuid4()


def cache_user_data(*args, **kwargs) -> None:
    """
    :param list or tuple args: This argument is a key of a cache.
    :param dict kwargs: This argument is a value of the cache.
    :return: void
    """
    log_t = "[task cache_user_data]:"
    from django.template.loader import render_to_string

    from persons.services import Cacher

    # ============================================
    # CACHE SERVER
    # ============================================
    cacher = Cacher(db=1)
    cacher.related()
    connected = cacher.connected
    # Checking of connection
    if not cacher.is_connected:
        error_t = " ".join([log_t, " Connecting to the cache server has not exists."])
        log.error(error_t)
        return

    # Here we make to cache of data.
    try:
        with connected() as conn:
            log.warning("[task cache_user_data]: Before caching the new data")
            log.warning("[task cache_user_data]: DEBUG TEST: %s" % args[0])
            k = str(args[0])
            conn.setex(k, 300, json.dumps(kwargs, ensure_ascii=False).encode("utf-8"))
            log.warning("[task cache_user_data]: Data was cached successfully!")

    except Exception as e:
        log.error(e)
        return

    # try:
    #     # ============================================
    #     # LETTER TO THE USER'S EMAIL
    #     # ============================================
    #     text_context = render_to_string(
    #         "account/email/email_confirmation_signup_message.txt"
    #     )
    #     subject = "Test Email message"
    #     send_mail(subject, text_context, [to_email], APP_DEFAULT_FROM_EMAIL, )
    # except Exception as e:
    #     error_t = " ".join([log_t, f" TEXT_ERROR: {e.args[0] if e.args else str(e)}"])
    #     log.error(error_t)


@shared_task(
    name="task_caching_before_verification",
    bind=True,
    ignore_result=True,
    autoretry_for=(TimeoutError, ConnectionError, OSError, Exception),
    retry_backoff=True,
    max_retries=3,
    retry_backoff_max=30,
)
def task_caching_before_verification(self, *args, **kwargs) -> None:
    """
    This is a task, from the Celery, for caching purposes from the persons.
    :param self: This is setting from the Celery.
    :param list or tuple args: This is data for caching.
    :param dict kwargs: This is data for caching.
    :return: void
    """
    log_t = "[task_caching_before_verification]:"
    args_len = len(*args)
    kwargs_len = len(kwargs) if kwargs is not None else 0
    log.warning(log_t + f" LOG DEBUG args_len: {args_len}, kwargs_len: {kwargs_len}")
    if args_len > 0 and kwargs_len > 0:
        log.warning(log_t + " LOG DEBUG Key or value is valid. Before loop.")
        custom_loop = CustomizationSyncAsyncLoop(args, kwargs)
        custom_loop.get_new_function = cache_user_data
        wrapper = custom_loop.get_new_loop()
        wrapper()
        log.warning(log_t + " LOG DEBUG Task pass successfully!")
    else:
        log.error("[task_caching_before_verification]: Key or value is not valid.")
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
