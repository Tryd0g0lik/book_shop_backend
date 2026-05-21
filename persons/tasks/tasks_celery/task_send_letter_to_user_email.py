"""
persons/tasks/tasks_celery/task_send_letter_to_user_email.py:1
"""

import asyncio
import json
import logging
import queue
import time

from celery import shared_task

log = logging.getLogger(__name__)


# Here we make a work of the Postman.
# ============================================
# 1. GET ARRAY OF KEYS FROM THE CACHE
# ============================================
async def child_process_get_keys_0(
    key_pattern: str,
    log_t: str,
    queue: queue.Queue,
) -> bool:
    """
    :param str key_pattern: This is a pattern of the cache's key
    :param str log_t: This is simple the prefix text (subtext) for a log row/line.
    :param queue.Queue queue: This is the queue.Queue object.
    :return: list
    """
    from datetime import datetime

    from persons.apps import cachemanager

    try:
        log.info(
            log_t[:-1]
            + f"[{child_process_get_keys_0.__name__}]:"
            + """\n
# ============================================
# REDIS CACHE SERVER - GET THE COLLECTION of KEYS
# ============================================"""
        )
        keys: list = []
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
                    + " DEBUG THe KEY: %s RUN TO THE LOOP " % (key.decode("utf-8"),),
                )
                tasks.append(
                    asyncio.create_task(
                        cachemanager.aget(
                            queue_collection=queue, key=key.decode("utf-8")
                        )
                    )
                )
            await asyncio.gather(*tasks, return_exceptions=True)

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

    except Exception as e:
        error_t = log_t[:-1] + "[child_process_get_keys_0] ERORR_TEXT: %s" % str(e)
        log.error(error_t)
        print(error_t)
        return False
    return True


# ============================================
# 2. LETTER FOR USER (don't a working)
# ============================================
def child_process_send_letter_to_user_email_2(*args, **kwargs) -> bool:
    # from django.template.loader import render_to_string
    # from wagtail.admin.mail import send_mail
    # from persons import EnumEmailLetter
    log_t = f"[{child_process_send_letter_to_user_email_2.__name__}]:"

    log.info("DEBUG CHECK THE PATH TO THE LETTER %s" % args[0])
    try:
        log.info(
            log_t
            + """\n
# ============================================
# LETTER FOR THE USER'S EMAIL
# ============================================
        """
        )

        # text_context = render_to_string(
        #     EnumEmailLetter.CONFIRM_EMAIL_Letter_0.value
        # )
        pass
        # subject = "Test Email message"
        # send_mail(subject, text_context, [to_email], APP_DEFAULT_FROM_EMAIL, )
    except Exception as e:
        error_t = " ".join([log_t, f" TEXT_ERROR: {e.args[0] if e.args else str(e)}"])
        log.error(error_t)
        return False
    return True


async def send_letter_to_user_email(*args, **kwargs) -> bool:
    """
    TODO SEND the letter to user
    :param args:
    :param kwargs:
    :return:
    """
    log_t = f"[task {send_letter_to_user_email.__name__}]:"
    import asyncio

    keys_queue = queue.Queue(2000)

    lock = asyncio.Lock()
    list_of_results = []
    result_bool = False
    try:
        args_str: str = args[0]
        log.info(
            log_t
            + """ \n
----------------- child_process_get_keys_0  process --------------------"""
        )
        async with lock:
            result_bool = await child_process_get_keys_0(
                key_pattern=args_str % "*", queue=keys_queue, log_t=log_t
            )
        log.info(
            log_t
            + """ \n
------------------ /child_process_get_keys_0 process -------------------"""
        )
        log.info(
            log_t
            + """ \n
------------------ Result -------------------"""
        )
        log.info(
            log_t
            + """\n
We have the DATA in QUEUES (the JSON format). These data we above received.
Below we need t get the token. Then insert in letter and send.
        """
        )
        qsize = keys_queue.qsize()
        byte_code = None
        json_code = None
        if result_bool and qsize:
            try:
                while not keys_queue.empty():
                    byte_code = keys_queue.get_nowait()
                    json_code = json.loads(byte_code.decode("utf-8"))
                    list_of_results.append(json_code)

            except queue.Empty as e:
                log.warning(log_t + "WARNING QUEUE EMPTY TEXT => %s" % str(e))
                list_of_results.append(None)
        # The clean storage
        del qsize, byte_code, json_code
        if list_of_results[0] is not None:
            new_results_list = [
                item_json for item_json in list_of_results if item_json is not None
            ]
            list_of_results.clear()
            list_of_results.extend(new_results_list[:])
            # the clea storage
            del new_results_list

            log.info(
                log_t
                + """ \n
------------------ /Result -------------------"""
            )
    except Exception as e:
        log.error(log_t + "ERROR TEXT => %s" % str(e))
        return False

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
def task_postman(self, *args: tuple | list, **kwargs: dict) -> None:
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
    args_len = len(args)
    kwargs_len = len(kwargs) if kwargs is not None else 0
    if args_len > 0 and kwargs_len > 0:
        print(log_t + " START TASK POSTMAN ====.")
        log.info(log_t + "*ARGS: %s & **KWARGS: %s" % (str(args), str(kwargs)))
        custom_loop = CustomizationSyncAsyncLoop(args, kwargs)
        custom_loop.get_new_function = send_letter_to_user_email
        wrapper = custom_loop.get_new_loop()
        Thread(target=wrapper).start()

        print("[task postman]: TEST DEBUG TASK POSTMAN ====.")
    else:
        time.sleep(3)
    return
