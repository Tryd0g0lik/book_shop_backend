"""
persons/tasks/tasks_celery/task_send_letter_to_user_email.py:1
"""

import json
import logging
import time
from threading import Thread

from celery import shared_task

from persons.services import CustomizationSyncAsyncLoop

log = logging.getLogger(__name__)


async def send_letter_to_user_email(*args: tuple, **kwargs: dict) -> list:
    log_t = "[task send_letter_to_user_email]:"
    import queue
    from concurrent.futures import ThreadPoolExecutor
    from threading import Semaphore

    from django.template.loader import render_to_string

    keys_queue = queue.Queue(2000)
    semaphore = Semaphore(4)

    # Here we make a work of the Postman.
    # ============================================
    # 1. GET ARRAY OF KEYS FROM THE CACHE
    # ============================================
    def child_process(key_pattern: str, num: int = 1) -> list:
        from persons.services import Cacher

        data_from_cache = []

        # ============================================
        # CACHE SERVER
        # ============================================
        cacher = Cacher(db=num)
        cacher.related()
        connected = cacher.connected
        # Checking of connection.
        if not cacher.is_connected:
            error_t = " ".join(
                [log_t, " Connecting to the cache server has not exists."]
            )
            log.error(error_t)
            print("\nERROR " + error_t)
            return [0]
        try:

            with connected() as conn:
                # Get keys from the cache.
                keys = []
                try:
                    log.info("[task cache_user_data]: Before lookup the keys of cache.")
                    print(
                        "\n[task cache_user_data]: DEBUG Before lookup the keys of cache."
                    )
                    keys.insert(len(keys), conn.keys(key_pattern))
                    log.info("[task cache_user_data]: Data was cached successfully!")
                    print("[task cache_user_data]: DEBUG Data was cached successfully!")

                except queue.Full as e:
                    log.warning("[task cache_user_data]: %s" % str(e))
                    print("[task cache_user_data]:DEBUG %s" % str(e))
                    keys.insert(len(keys), conn.keys(key_pattern))
                except Exception as e:
                    log.error("[task cache_user_data]: %s" % str(e))
                    print("[task cache_user_data]: DEBUG %s" % str(e))
                    return []
                [keys_queue.put_nowait(key) for key in keys]
                print("[task cache_user_data]: DEBUG LEng %s" % str(keys_queue.qsize()))

                # Get the cache's data by the keys.
                try:
                    while keys_queue.qsize() > 0:
                        keys = keys_queue.get()
                        for key in keys:
                            log.info(
                                "[task cache_user_data]: TEST DEBUG KEY: %s" % str(key)
                            )
                            print(
                                "[task cache_user_data]: TEST DEBUG KEY: %s" % str(key)
                            )

                            with semaphore:
                                if key:
                                    res = conn.get(key.decode())

                                    log.info(
                                        "[task cache_user_data]: TEST DEBUG res: %s"
                                        % str(res)
                                    )
                                    print(
                                        "[task cache_user_data]: TEST DEBUG res: %s"
                                        % str(res)
                                    )
                                    if res:
                                        data_from_cache.append(
                                            json.loads(res.decode("utf-8"))
                                        )
                                    conn.delete(key.decode())
                                else:
                                    log.warning(f"{log_t} Key {key} has not value")

                except queue.Empty as e:
                    log.warning("[task cache_user_data]: %s" % str(e))
                    print("[task cache_user_data]: %s" % str(e))

        except Exception as e:
            error_t = "[task cache_user_data] ERORR_TEXT: %s" % str(e)
            log.error(error_t)
            print(error_t)
            return [1]
        return data_from_cache

    # ============================================
    # 2. GET DATA BY KEYS FROM THE CACHE
    # ============================================
    async def parent_process_get_data_of_user(*args) -> list | tuple:
        data_of_cache = []
        controller = True
        with ThreadPoolExecutor(max_workers=4) as executor:
            log.info(
                "[task cache_user_data]: TEST DEBUG Before loop. ARGS: %s" % str(args)
            )
            print(
                "\n[task cache_user_data]: TEST DEBUG Before loop. ARGS: %s" % str(args)
            )
            while controller:
                result_list: list | tuple = args[:]
                for pattern in result_list:
                    if type(pattern) is list:
                        (args.insert(len(args), pattern),)
                        continue
                    elif type(pattern) is tuple:
                        args += pattern
                        continue
                    else:
                        controller = False
                    log.info(
                        "[task cache_user_data]: TEST DEBUG pattern: %s" % str(pattern)
                    )
                    print(
                        "[task cache_user_data]: TEST DEBUG pattern: %s" % str(pattern)
                    )
                    if pattern:
                        data_of_cache.append(
                            {pattern: executor.submit(child_process, pattern)}
                        )
            if len(data_of_cache) == 0:
                log.warning(f"{log_t} No patterns provided")
                print(f"{log_t} No patterns provided")
                return [2]
            return data_of_cache

    get_data_of_cache = await parent_process_get_data_of_user(args[0])
    return get_data_of_cache[0]
    # log.info("DEBUG CHECK THE PATH TO THE LETTER %s" % args[0])
    # try:
    #     # ============================================
    #     # LETTER TO THE USER'S EMAIL
    #     # ============================================
    #     text_context = render_to_string(
    #         pass
    #     )
    #     subject = "Test Email message"
    #     send_mail(subject, text_context, [to_email], APP_DEFAULT_FROM_EMAIL, )
    # except Exception as e:
    #     error_t = " ".join([log_t, f" TEXT_ERROR: {e.args[0] if e.args else str(e)}"])
    #     log.error(error_t)


@shared_task(
    name="task_get_send_letter",
    bind=True,
    ignore_result=True,
    autoretry_for=(TimeoutError, ConnectionError, OSError, Exception),
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
    log_t = "[task_postman]:"
    args_len = len(args)
    kwargs_len = len(kwargs) if kwargs is not None else 0
    if args_len > 0 and kwargs_len > 0:
        print(log_t + " START TASK POSTMAN ====.")

        custom_loop = CustomizationSyncAsyncLoop(*args, **kwargs)
        custom_loop.get_new_function = send_letter_to_user_email
        wrapper = custom_loop.get_new_loop()
        Thread(target=wrapper).start()
        print("[task postman]: TEST DEBUG TASK POSTMAN ====.")
    else:
        time.sleep(2)
    return
