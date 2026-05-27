"""
persons/tasks/tasks_celery/task_send_letter_to_user_email.py:1
"""

import asyncio
import json
import logging
import queue
import time

from celery import shared_task

from persons import EnumTemplatesKeysCache
from persons.tasks.sub_tasks_celery.sub_task_get_send_letter import (
    task_child_process_letter_Thanks_for_your_account,
)

log = logging.getLogger(__name__)


# Here we make a work of the Postman.
# ============================================
# 1. GET ARRAY OF KEYS FROM THE CACHE
# ============================================
async def child_process_get_keys_0(
    lock: asyncio.Lock,
    key_pattern: str,
    log_t: str,
    queue: queue.Queue,
) -> bool:
    """
    TODO: Можно получить из кеша, можно сохранить в кеше, продлить срок жизни ключа .
        В строке 'queue_collection=queue, key=key.decode("utf-8")' передаём очередь.
        В эту очередь добавляем рузельтат отработанных данных из keys.
        Надо вставить логику которая будет отслеживать - какие данные из keys успел отработать (до того как queue получила
        максимальную длину) а какие ключи не спела. Иначе потеляю данные и BACKOFF просто начнёт работу заного с теми
        же ключами и в том же количестве.
    Here we are creating a queue of tasks. Everyone task it is a request to the cache Radis's server.
    We collect all the result in the queue.
    :param asyncio.Lock lock: It is beholder.
    :param str key_pattern: This is a pattern of the cache's key
    :param str log_t: This is simple the prefix text (subtext) for a log row/line.
    :param queue.Queue queue: This is the queue.Queue object.
    :return: list
    """
    from datetime import datetime

    from persons.apps import cachemanager

    keys: list = []
    try:
        log.info(
            log_t[:-1]
            + f"[{child_process_get_keys_0.__name__}]:"
            + """\n
        # ============================================
        # REDIS CACHE SERVER - GET THE COLLECTION of KEYS
        # ============================================"""
        )
        async with lock:
            result_bool: bool = await cachemanager.aget(
                key_pattern=key_pattern,
                collection=keys,
            )
            log.warning(
                log_t[:-1]
                + f"[{child_process_get_keys_0.__name__}]:"
                + " DEBUG \nReceived key_pattern %s \n & LIST LENGTH: %s & LIST: %s \n  RESULT_BOOL: %s "
                % (key_pattern, str(len(keys)), str(keys), str(result_bool))
            )
            start_time = datetime.now()
            if result_bool:
                tasks = []

                for key in keys:
                    log.warning(
                        log_t[:-1]
                        + f"[{child_process_get_keys_0.__name__}]:"
                        + " DEBUG THe KEY: %s RUN TO THE LOOP "
                        % (key.decode("utf-8"),),
                    )
                    tasks.append(
                        asyncio.create_task(
                            cachemanager.aget(
                                queue_collection=queue, key=key.decode("utf-8")
                            )
                        )
                    )
                await asyncio.gather(*tasks, return_exceptions=True)

        log.info(
            log_t[:-1]
            + f"[{child_process_get_keys_0.__name__}]: ====================== DEBUG Review ======================"
        )
        end_time = datetime.now()
        passed_time: datetime.now = end_time - start_time
        log.info(
            " ".join([log_t[:-1], f"[{child_process_get_keys_0.__name__}]:", "Time:"])
        )
        # Simple the overview by values
        log_t = " ".join(
            [
                log_t[:-1],
                f"[{child_process_get_keys_0.__name__}]:",
                f"\nStart: {start_time.strftime('%Y-%m-%d %H:%M:%S')}",
                f"\nEnd: {end_time.strftime('%Y-%m-%d %H:%M:%S')}",
                f"\nPassed: {passed_time}",
                f"\nResult size: {queue.qsize()}",
                f"\nResult : {str(queue)}",
            ]
        )

        log.info(log_t)
        log.info(
            log_t[:-1]
            + f"[{child_process_get_keys_0.__name__}]: ====================== /DEBUG Review ======================"
        )

    except Exception as e:
        error_t = log_t[:-1] + "[child_process_get_keys_0] ERORR_TEXT: %s" % str(e)
        log.error(error_t)
        raise e
    return True


# ============================================
# THE SUB FUNCTION IS TO AVOID A CODE DUPLICATION, below/
# ============================================
def sub_function(keys_queue, log_t, result_bool):
    list_of_results = []
    qsize = keys_queue.qsize()
    if result_bool and qsize:
        while not keys_queue.empty():
            byte_code = keys_queue.get_nowait()
            json_code = json.loads(byte_code.decode("utf-8"))
            list_of_results.append(json_code)

    # The clean storage
    del qsize
    if len(list_of_results) == 0:
        log.warning(
            log_t
            + "Queue empty. Maybe what wrong! Length of list: %s "
            % len(list_of_results)
        )
        return False

    task_child_process_letter_Thanks_for_your_account.delay(*(list_of_results,), {})
    return True


async def send_letter_to_user_email(*args, **kwargs) -> bool:
    """
    First - we should send q queue in side the child_process_get_keys_0 of sub-function.
    This sub-function should return the full queue. This queue should contain tha cache's data of JSON-str.
    The MAX length of queue - 2000 items,
    :param args:
    :param kwargs:
    :return:
    """
    log_t = f"[task {send_letter_to_user_email.__name__}]:"
    import asyncio

    log.info(f"DEBUG args: {args}")
    keys_queue = queue.Queue(2000)

    lock = asyncio.Lock()
    result_bool = False

    try:
        for args_str in args:
            log.info(log_t + """ \n BEFORE IS RUNNING THE child_process_get_keys_0""")
            async with lock:
                result_bool = await child_process_get_keys_0(
                    lock,
                    key_pattern=EnumTemplatesKeysCache.USER_PENDING_0.value % "*",
                    queue=keys_queue,
                    log_t=log_t,
                )
            log.info(
                log_t
                + """\n
    We have the DATA in QUEUES (the JSON format). These data we above received.
    Below we need t get the token. Then insert in letter and send.
            """
            )

            sub_function(keys_queue, log_t, result_bool)
    except queue.Full:
        sub_function(keys_queue, log_t, result_bool)
        raise

    except Exception as e:
        log.error(log_t + "ERROR TEXT => %s" % str(e))
        raise e

    return True


@shared_task(
    name="task_get_send_letter",
    bind=True,
    ignore_result=True,
    autoretry_for=(TimeoutError, ConnectionError, OSError),
    retry_backoff=True,
    max_retries=3,
    retry_backoff_max=30,
)
def task_postman(self, *args, **kwargs) -> None:
    """
    This is a task, from the Celery of Postman.
    Here these tasks are sending letters to the user's emails.
    :param self: This is setting from the Celery.
    :param list or tuple args: Here contain a key of the cache.
    :param dict kwargs: This tuple/list contain the key of the cache. This data is address to the template of letter.
    :return: void
    """
    from threading import Thread

    from persons.services import CustomizationSyncAsyncLoop

    log_t = "[task_postman]:"
    try:

        args_len = len(args)
        kwargs_len = len(kwargs) if kwargs is not None else 0
        if args_len > 0 and kwargs_len > 0:
            log.info(
                log_t + "DEBUG *ARGS: %s & **KWARGS: %s" % (str(args), str(kwargs))
            )
            custom_loop = CustomizationSyncAsyncLoop(*args, **kwargs)
            custom_loop.get_new_function = send_letter_to_user_email
            wrapper = custom_loop.get_new_loop()
            log.info(
                log_t + " After opening a new loop. & Before run the threading.Thread."
            )
            Thread(target=wrapper).start()
        else:
            time.sleep(3)
        return
    except Exception as e:
        log.info(log_t + str(e))
        raise self.retry(exc=e, countdown=30)
