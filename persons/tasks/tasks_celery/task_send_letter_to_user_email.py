"""
persons/tasks/tasks_celery/task_send_letter_to_user_email.py:1
"""

import asyncio
import json
import logging
import queue
import re
import time
from typing import Any, Mapping, Optional, Union

from celery import shared_task

from persons import EnumEmailLetter, EnumTemplatesKeysCache, EnuSubjectOfLetter
from persons.exceptions import PersonErrorTasks
from persons.interfaces import PostmanAdapter
from persons.interfaces.interface_persons import UsersPydantic, UsersPydanticDict

# from persons.tasks.sub_tasks_celery.sub_task_get_send_letter import (
#     child_process_emailing,
#     task_child_process_letter_thanks_for_your_account,
# )

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
    TODO: Можно получить из кеша, можно сохранить в кеше, продлить срок жизни ключа .
        В строке 'queue_collection=queue, key=key.decode("utf-8")' передаём очередь.
        В эту очередь добавляем рузельтат отработанных данных из keys.
        Надо вставить логику которая будет отслеживать - какие данные из keys успел отработать (до того как queue получила
        максимальную длину) а какие ключи не спела. Иначе потеляю данные и BACKOFF просто начнёт работу заного с теми
        же ключами и в том же количестве.
    Here we are creating a queue of tasks. Every task it is a request to the cache Radis's server.
    We collect all result in the queue.
    :param asyncio.Lock lock: It is beholder.
    :param str key_pattern: This is a pattern of the cache's key
    :param str log_t: This is simple the prefix text (subtext) for a log row/line.
    :param queue.Queue queue: This is the queue.Queue object.
    :return: list
    """
    from datetime import datetime

    from persons.interfaces import CacheManager as CacheManagerInitialize
    from persons.services import AccountManager

    account_manager = AccountManager()
    postman = account_manager.postman
    SubPerson = postman.SubPerson
    sub_person = SubPerson()
    keys: list = []
    try:
        log.info(
            log_t[:-1]
            + f"""[{child_process_get_keys_0.__name__}]: \n
        # ============================================
        # REDIS CACHE SERVER - BEFORE  THE GET COLLECTION BY THE TEMPLATE of KEYS
        # - key_pattern: {str(key_pattern)}
        # - keys: {str(keys)}
        # ============================================"""
        )

        result_bool: bool = await sub_person.cachemanager.aget(
            key_pattern=key_pattern,
            collection=keys,
        )
        log.warning(
            log_t[:-1]
            + f""""[{child_process_get_keys_0.__name__}]: \n
        # ============================================
        # DEBUG REDIS CACHE SERVER - AFTER  THE GET COLLECTION BY THE TEMPLATE of KEYS
        # Received key_pattern %s \n# LIST LENGTH: %s
        # LIST: %s \n# RESULT_BOOL: %s
        # ============================================
"""
            % (key_pattern, str(len(keys)), str(keys), str(result_bool))
        )
        start_time = datetime.now()
        if result_bool:
            tasks = []

            for key in keys:
                log.warning(
                    log_t[:-1]
                    + f"[{child_process_get_keys_0.__name__}]:"
                    + """\n
        # ============================================
        # DEBUG REDIS CACHE SERVER - BEFORE  THE GET COLLECTION BY THE KEY of POSITION
        # THe KEY: %s
        # ============================================
        """
                    % (key.decode("utf-8"),),
                )
                tasks.append(
                    asyncio.create_task(
                        sub_person.cachemanager.aget(
                            queue_collection=queue, key=key.decode("utf-8")
                        )
                    )
                )
            await asyncio.gather(*tasks, return_exceptions=True)
        log.info(
            log_t[:-1]
            + f"[{child_process_get_keys_0.__name__}]:"
            + """\n
        # ============================================
        # DEBUG REDIS CACHE SERVER - AFTER  THE GET COLLECTION BY THE KEY of POSITION
        # THe FOUND CACHE'S POSITIONS: %s
        # ============================================
        """
            % queue.qsize()
        )

        log.info(
            log_t[:-1]
            + f"[{child_process_get_keys_0.__name__}]:\n ====================== DEBUG Review ======================"
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
            + f"[{child_process_get_keys_0.__name__}]: \n ====================== /DEBUG Review ======================"
        )

    except Exception as e:
        error_t = log_t[:-1] + "[child_process_get_keys_0] ERORR_TEXT: %s" % str(e)
        log.error(error_t)
        raise PersonErrorTasks(e.args[0] if len(e.args) else str(e))
    return True


# ============================================
# THE SUB FUNCTION IS TO AVOID A CODE DUPLICATION, below/
# ============================================
def sub_function(
    list_of_keys: list,
    log_t: str,
    subject_: str,
    text_context_: str,
    context_: Optional[Mapping[str, Any]],
) -> Union[list | bool]:
    """
    :param queue keys_queue: Required.
    :param str log_t: Required. It is a prefix for the logs.
    :param result_bool: Required.
    :param str subject_: Required. It is thema/heading for a letter.
    :param str text_context_: Required. It is massage in the letter body
    :param Optional[Mapping[str, Any]] context_: It is acontext data from the letter body.
    :return:
    """
    from persons.tasks.sub_tasks_celery.sub_task_get_send_letter import (
        child_process_emailing,
    )

    # keys_queue: queue = test_keys_queue
    log_t = log_t[:-1] + "[test sub_function]:"

    kwargs = {"subject": subject_, "text_context": text_context_, "context": context_}
    # task_child_process_letter_thanks_for_your_account.delay(*(list_of_keys,), **kwargs)
    child_process_emailing(*(list_of_keys,), **kwargs)
    log.info(
        log_t[:-1]
        + f"[{sub_function.__name__}]:"
        + " Data has been transmitted next for sending in a email address."
    )

    return list_of_keys


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

    from persons.services import AccountManager, CacheManager

    dict_queue = queue.Queue(2000)
    list_of_keys = []
    lock = asyncio.Lock()
    result_bool = False
    subject: str = EnuSubjectOfLetter.SUB_TASK_GET_SEND_LETTER_0.value
    context_: Optional[Mapping[str, Any]] = None
    try:
        # emails = [v for k, v in kwargs.items() if k == "email"]
        # key_cache = list(args)[0]
        # for one_email in emails:

        async with lock:
            result_bool = await child_process_get_keys_0(
                key_pattern=EnumTemplatesKeysCache.USER_PENDING.value % "*",
                queue=dict_queue,
                log_t=log_t,
            )
        log.info(
            log_t
            + f"""\n
            # ============================================
We have the DATA in QUEUES (the JSON format). These data we above received.
Below we need t get the token. Then insert in letter and send.
            # dict_queue: {dict_queue.qsize()}
            # ============================================
        """
        )

        qsize = dict_queue.qsize()
        log.info(f"DDEBUG sub_function: 0 qsize: {qsize}")
        if result_bool and qsize:
            while not dict_queue.empty():
                byte_code = dict_queue.get_nowait()
                json_code = json.loads(byte_code.decode("utf-8"))
                list_of_keys.append(json_code)
        else:
            return False
        account_manager = AccountManager()

        # Below we are transmitting data for a email verification.
        postman = account_manager.postman

        for one_dict in list_of_keys:
            one_email = one_dict.get("email")

            # key_cache = EnumTemplatesKeysCache.USER_PENDING_LETTER.value
            sub_person = postman.SubPerson(
                person_email=one_email,
            )
            database_service = postman.database_service
            key_cache = EnumTemplatesKeysCache.USER_PENDING.value % re.sub(
                r"[@.]+", "", one_email
            )
            log.info(
                log_t
                + f""" \n
                # ============================================
                # BEFORE IS RUNNING THE child_process_get_keys_0,
                # args_str: {one_email}
                # key_cache: {key_cache}
                # ============================================
"""
            )

            person_list: Optional[list[UsersPydanticDict]] = await sub_person.get_model(
                database_service, key_cache
            )
            log.info(
                f"""
                # ============================================
                # DEBUG
                # person_list: {str(person_list)}
                # Type: {type(person_list)}
                # ============================================
"""
            )
            account_manager = account_manager.inisialize_account()
            for person_dict in person_list:
                # Here we are transmitting data for mailing, Here we are speak obout the new account.
                log.info(
                    f"DEBUG person_dict: {str(person_dict)} & Type: {type(person_dict)}"
                )

                text_context: str = EnumEmailLetter.CONFIRM_EMAIL_Letter_0.value
                sub_function(
                    list_of_keys,
                    log_t,
                    subject,
                    text_context,
                    None,
                )

                text_context: str = EnumEmailLetter.CONFIRM_EMAIL_Letter_1.value
                generate_login_code = account_manager.generate_login_code()
                log.info(f"DEBUG generate_login_code: {generate_login_code}")
                context_ = {
                    "user": json.dumps(person_dict),
                    "code": generate_login_code,
                }
                log.info(f"DEBUG context_: {str(context_)} & Type: {type(context_)}")
                sub_function(
                    list_of_keys,
                    log_t,
                    subject,
                    text_context,
                    context_,
                )

                del result_bool, text_context, context_
    except queue.Full:

        raise

    except Exception as e:
        log.error(log_t + "ERROR TEXT => %s" % str(e))
        raise PersonErrorTasks(e.args[0] if len(e.args) else str(e))

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
        custom_loop = CustomizationSyncAsyncLoop(*args, **kwargs)
        custom_loop.get_new_function = send_letter_to_user_email
        wrapper = custom_loop.get_new_loop()
        log.info(
            log_t + " After opening a new loop. & Before run the threading.Thread."
        )
        Thread(target=wrapper).start()

        time.sleep(3)

    except Exception as e:
        log.info(log_t + str(e))
        raise self.retry(exc=e, countdown=30)
