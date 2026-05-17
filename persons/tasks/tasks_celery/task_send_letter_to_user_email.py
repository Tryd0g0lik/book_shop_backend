"""
persons/tasks/tasks_celery/task_send_letter_to_user_email.py:1
"""

import asyncio
import concurrent.futures
import json
import logging
import queue
import time

from celery import shared_task

# from persons.services import CustomizationSyncAsyncLoop

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
    # import concurrent.futures
    from datetime import datetime

    from persons.apps import cachemanager

    # from persons.services import CustomizationSyncAsyncLoop

    try:
        log.info(
            log_t[:-1]
            + f"[{child_process_get_keys_0.__name__}]:"
            + """\n
============================================
# REDIS CACHE SERVER - GET THE COLLECTION of KEYS
# ============================================"""
        )
        keys: list = []
        # futures: list = []
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
                # kwargs = {"queue_collection": queue, "key": key.decode("utf-8")}

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
        # future = ()

        # async with lock:
        #     async with asynccacher.connected() as conn:

        # # Get keys from the cache.
        # try:
        #     log.info(log_t[:-1] + " [child_process_get_keys_0]: Before lookup the keys of cache.")
        #     print(
        #         "\n[child_process_get_keys_0]: DEBUG Before lookup the keys of cache."
        #     )
        #     # Get the cache's data by the keys.
        #     queue.put_nowait(conn.keys(key_pattern))
        #     log.info(log_t[:-1] + "[child_process_get_keys_0]: Data was cached successfully!")
        #     print("[child_process_get_keys_0]: DEBUG Data was cached successfully!")
        #
        # except queue.Full as e:
        #     log.warning(log_t[:-1] + "[child_process_get_keys_0]: %s" % str(e))
        #     print("[child_process_get_keys_0]: DEBUG %s" % str(e))
        #     queue.put(conn.keys(key_pattern))
        # except Exception as e:
        #     log.error(log_t[:-1] + "[child_process_get_keys_0]: %s" % str(e))
        #     print("[child_process_get_keys_0] DEBUG %s" % str(e))
        #     return False
        # log.info(log_t[:-1] + "[child_process_get_keys_0]: all successfully was saved in the queue.")
        # print("[child_process_get_keys_0]: all successfully was saved in the queue.")

    except Exception as e:
        error_t = log_t[:-1] + "[child_process_get_keys_0] ERORR_TEXT: %s" % str(e)
        log.error(error_t)
        print(error_t)
        return False
    return True


def child_process_send_letter_to_user_email_2():
    from django.template.loader import render_to_string
    from wagtail.admin.mail import send_mail

    pass
    # log.info("DEBUG CHECK THE PATH TO THE LETTER %s" % args[0])
    # try:
    #     # ============================================
    #     # LETTER TO THE USER'S EMAIL
    #     # ============================================
    #     text_context = render_to_string(
    #         EnumEmailLetter.CONFIRM_EMAIL_Letter_0.value
    #     )
    #
    #     subject = "Test Email message"
    #     send_mail(subject, text_context, [to_email], APP_DEFAULT_FROM_EMAIL, )
    # except Exception as e:
    #     error_t = " ".join([log_t, f" TEXT_ERROR: {e.args[0] if e.args else str(e)}"])
    #     log.error(error_t)
    # return get_data_of_cache[0]


async def send_letter_to_user_email(*args, **kwargs) -> list:
    log_t = f"[task {send_letter_to_user_email.__name__}]:"
    from concurrent.futures import ThreadPoolExecutor
    from threading import Semaphore

    from persons import EnumEmailLetter, EnumTemplatesKeysCache

    keys_queue = queue.Queue(2000)
    # semaphore = Semaphore(4)
    # lock = asyncio.Lock()
    list_of_results = []
    try:
        # while keys_queue.qsize() > 0:
        # keys = keys_queue.get()
        # with semaphore:
        # for key in keys:
        args_str: str = args[0]
        log.info(
            log_t
            + " \n----------------- child_process_get_keys_0  process --------------------"
        )
        result_bool = await child_process_get_keys_0(
            key_pattern=args_str % "*", queue=keys_queue, log_t=log_t
        )
        log.info(
            log_t
            + " \n------------------ /child_process_get_keys_0 process -------------------"
        )
        log.info(log_t + " \n------------------ Result -------------------")
        qsize = keys_queue.qsize()
        if result_bool and qsize:
            try:
                while not keys_queue.empty():
                    byte_code = keys_queue.get_nowait()
                    json_code = json.loads(byte_code.decode("utf-8"))
                    list_of_results.append(json_code)
            except queue.Empty as e:
                list_of_results.append(None)
                log.warning(log_t + "WARNING QUEUE EMPTY TEXT => %s" % str(e))
            log.info(log_t + " \n------------------ /Result -------------------")

            log.info(log_t + "RESULT BOOL => %s" % str(result_bool))
            log.info(log_t + "RESULT DATA SIZE QUEUE=> %s" % str(qsize))
            log.info(log_t + "RESULT DATA QUEUE => %s" % str(list_of_results))
    except Exception as e:
        log.error(log_t + "ERROR TEXT => %s" % str(e))
        return []

    return list_of_results
    # # ============================================
    # # 2. GET DATA BY KEYS FROM THE CACHE
    # # ============================================
    # async def parent_process_get_data_of_user(*args) -> list | tuple:
    #
    #     data_of_cache = []
    #     controller = True
    #     with ThreadPoolExecutor(max_workers=4) as executor:
    #         log.info(
    #             "[task cache_user_data]: TEST DEBUG Before loop. ARGS: %s" % str(args)
    #         )
    #         print(
    #             "\n[task cache_user_data]: TEST DEBUG Before loop. ARGS: %s" % str(args)
    #         )
    #         while controller:
    #             result_list: list | tuple = args[:]
    #             for pattern in result_list:
    #                 if type(pattern) is list:
    #                     (args.insert(len(args), pattern),)
    #                     continue
    #                 elif type(pattern) is tuple:
    #                     args += pattern
    #                     continue
    #                 else:
    #                     controller = False
    #                 log.info(
    #                     "[task cache_user_data]: TEST DEBUG pattern: %s" % str(pattern)
    #                 )
    #                 print(
    #                     "[task cache_user_data]: TEST DEBUG pattern: %s" % str(pattern)
    #                 )
    #                 if pattern:
    #                     data_of_cache.append(
    #                         {pattern: executor.submit(child_process, pattern)}
    #                     )
    #         if len(data_of_cache) == 0:
    #             log.warning(f"{log_t} No patterns provided")
    #             print(f"{log_t} No patterns provided")
    #             return [2]
    #         return data_of_cache
    #
    # get_data_of_cache = await parent_process_get_data_of_user(args[0])
    #

    # child_process_send_letter_to_user_email_2()


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
