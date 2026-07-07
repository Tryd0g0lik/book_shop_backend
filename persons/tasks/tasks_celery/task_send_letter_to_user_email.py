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
from django.core.mail import send_mail
from django.template.loader import render_to_string

from persons import EnumEmailLetter, EnuSubjectOfLetter
from persons.exceptions import PersonErrorTasks
from persons.tasks.tasks_celery.task_create_position import (
    task_create_position_for_EmailConfiguration,
)
from project.settings_conf.settings_env import APP_DEFAULT_FROM_EMAIL
from project.settings_conf.settings_first import DEFAULT_CHARSET

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
    from utilities.services import CacheManager

    log_t = log_t[:-1] + f"[{child_process_get_keys_0.__name__}]:"
    cachemanager = CacheManager()
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

        result_bool: bool = await cachemanager.aget(
            key_pattern=key_pattern,
            collection=keys,
        )
        log.info(
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
        tasks = []
        if result_bool:

            for key in keys:
                key = key.decode(DEFAULT_CHARSET)
                if ":letter:" in key:
                    continue
                log.info(
                    log_t[:-1]
                    + f"[{child_process_get_keys_0.__name__}]:"
                    + """\n
                    # ============================================
                    # DEBUG REDIS CACHE SERVER - BEFORE  THE GET COLLECTION BY THE KEY of POSITION
                    # THe KEY: %s
                    # ============================================
                    """
                    % (key,),
                )
                tasks.append(
                    asyncio.create_task(
                        cachemanager.aget(queue_collection=queue, key=key)
                    )
                )
            await asyncio.gather(*tasks, return_exceptions=True)

        log.info(
            log_t[:-1]
            + f"[{child_process_get_keys_0.__name__}]:"
            + """\n
        # ============================================
        # DEBUG REDIS CACHE SERVER - AFTER  THE GETS COLLECTION KEYS FROM POSITIONS
        # THe FOUND CACHE'S POSITIONS: %s
        # ============================================
        """
            % queue.qsize()
        )
        tasks.clear()
        await cachemanager.asynccacher.related()

        async def resave_cache_after_sent_letter(*args) -> bool:
            """
            :param str args: It is the one old key of cache.

            :return:
            """
            from utilities import EnumTemplatesKeysCache

            lt = log_t[:-1] + f"[{resave_cache_after_sent_letter.__name__}]:"
            assert len(args) >= 1, "One or more keys"
            log.info(f"{lt} # test run {args}")
            for k in args:
                k = k.decode(DEFAULT_CHARSET)
                data_list: list = []

                try:
                    log.info(f"{lt} # It is receiving the user data")
                    await cachemanager.aget(key=k, collection=data_list, exat=1)
                    log.info("# New key for resaves")
                    key: str = (
                        EnumTemplatesKeysCache.USER_PENDING_LETTER.value
                        % k.split(":")[-1]
                    )
                    user_data_json = json.loads((data_list[0]).decode(DEFAULT_CHARSET))
                    if "verification_code" in user_data_json:
                        data_list.clear()
                        continue
                    data_list.clear()
                    log.info(lt + " User dada Re-saved user_data_json key !")
                    # Re-save
                    response_bool = await cachemanager.asave(
                        key=key, default=user_data_json, ttl=86400
                    )
                    log.info(lt + " User dada Re-saved successfully from old key !")
                    return response_bool

                except Exception as e:
                    log.error(lt + " ERROR => " + e.args[0] if e.args else str(e))
                    return False
            return True

        # assert type(keys) in (list, tuple), "Check the type"
        # assert len(keys) >= 1, "Check the count keys"

        for key in keys:
            log.info(f"[{child_process_get_keys_0.__name__}]: key: {key}")
            tasks.append(resave_cache_after_sent_letter(*(key,)))
        keys.clear()
        log.info(
            log_t[:-1]
            + f"""[{child_process_get_keys_0.__name__}]:\n
        # ============================================
        # BELOW RE-SAVES THE USER DATA THEN REMOVES KEYS
        # ============================================"""
        )
        await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        error_t = log_t[
            :-1
        ] + f"[{child_process_get_keys_0.__name__}]: ERORR_TEXT: %s" % str(e)
        log.error(error_t)
        raise PersonErrorTasks(e.args[0] if len(e.args) else str(e))
    return True


# ============================================
# THE SUB FUNCTION IS TO AVOID A CODE DUPLICATION, below/
# ============================================
def sub_function_send_mail(
    list_of_keys: list,
    subject_: str,
    text_context_: str,
    context_: Optional[Mapping[str, Any]],
) -> Union[list, bool]:
    """
    :param queue keys_queue: Required.
    :param str log_t: Required. It is a prefix for the logs.
    :param result_bool: Required.
    :param str subject_: Required. It is thema/heading for a letter.
    :param str text_context_: Required. It is massage in the letter body
    :param Optional[Mapping[str, Any]] context_: It is acontext data from the letter body.
    :return:
    """
    text_context = render_to_string(template_name=text_context_, context=context_)
    send_mail(
        subject=subject_,
        message=text_context,
        recipient_list=list_of_keys,
        from_email=APP_DEFAULT_FROM_EMAIL,
    )
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
    from datetime import datetime

    from django.contrib.auth import get_user_model

    from utilities import EnumTemplatesKeysCache

    Users = get_user_model()

    from allauth.account.adapter import DefaultAccountAdapter

    from utilities.services import AccountManager, CacheManager

    accountAdapter = DefaultAccountAdapter()
    dict_queue = queue.Queue(2000)
    list_of_keys = []
    lock = asyncio.Lock()
    subject: str = EnuSubjectOfLetter.SUB_TASK_GET_SEND_LETTER_0.value
    try:
        log.info(
            log_t
            + """
        # ============================================
        # HERE WE COLLECT CHECKING THE KEYS OF CACHE
        # ============================================"""
        )
        # async with lock:
        result_bool = await child_process_get_keys_0(
            key_pattern=EnumTemplatesKeysCache.USER_PENDING_ZERO.value % "*",
            queue=dict_queue,
            log_t=log_t[:],
        )
        qsize = dict_queue.qsize()

        if result_bool and qsize > 0:
            while not dict_queue.empty():
                byte_code = dict_queue.get_nowait()
                list_of_keys = json.loads(byte_code.decode(DEFAULT_CHARSET))

                # list_of_keys.append(json_code)
                # account_manager = AccountManager()
                # generater = account_manager.inisialize_account()
                log.info(
                    log_t
                    + f"""
                # ============================================
                # EVERY ONE KEY - IT NEED TO SEND THE TWO LETTER
                {list_of_keys}
                # ============================================"""
                )
                for one_dict in (
                    list_of_keys
                    if type(list_of_keys) in (list, tuple)
                    else [list_of_keys]
                ):
                    if "verification_code" in one_dict:
                        continue
                    one_email = one_dict.get("email")

                    person_queryset_filter = await asyncio.to_thread(
                        lambda: Users.objects.filter(email=one_email)
                    )
                    log.info(
                        "# Here we are transmitting data for mailing, Here we tell the user obout new account."
                    )
                    person_object: Users = await asyncio.to_thread(
                        lambda: person_queryset_filter.first()
                    )
                    context_ = {
                        "user": person_object,
                    }
                    async with lock:
                        text_context: str = EnumEmailLetter.CONFIRM_EMAIL_Letter_0.value
                        log.info("  < = > 0")
                        # --- Sending a letter
                        sub_function_send_mail(
                            [one_email],
                            subject,
                            text_context,
                            context_,
                        )
                        # --- Sending a letter second
                        log.info("# The First letter is gone")
                        text_context: str = EnumEmailLetter.CONFIRM_EMAIL_Letter_1.value
                        generate_login_code = (
                            accountAdapter.generate_email_verification_code()
                        )

                        context_ = {
                            "user": person_object,
                            "code": generate_login_code,
                        }
                        sub_function_send_mail(
                            [one_email],
                            subject,
                            text_context,
                            context_,
                        )

                        task_create_position_for_EmailConfiguration.delay(
                            one_email, generate_login_code
                        )
                        # ---

                        log.info(
                            log_t
                            + """
                        # ============================================
                        # INITIAL DATA WILL BE SAVING IN CACHE
                        # ============================================"""
                        )
                        cachemanager = CacheManager()
                        k: str = (
                            EnumTemplatesKeysCache.USER_PENDING_LETTER.value
                            % re.sub(r"[@.]+", "", one_email)
                        )
                        collection_: list[bytes] = []
                        # ---
                        await cachemanager.aget(key=k, collection=collection_, exat=1)
                        await cachemanager.asynccacher.close()

                        # ---
                        for one_dict in collection_:
                            user_data_json: dict = json.loads(
                                (one_dict).decode(DEFAULT_CHARSET)
                            )

                            user_data_json["verification_code"] = generate_login_code
                            log.info(
                                log_t
                                + f"# save a verification code user_data_json: {str(user_data_json)}"
                            )
                            await cachemanager.asave(
                                key=k, default=user_data_json, ttl=86400
                            )
                            await cachemanager.asynccacher.close()
                        # ---
                        log.info(
                            log_t
                            + """
                        # ============================================
                        # SAME DATA WILL BE SAVING IN DATABASE
                        # ============================================"""
                        )
                        person_object.is_sent = True
                        person_object.updated_at = datetime.now()
                        await asyncio.to_thread(
                            lambda: person_object.save(
                                update_fields=["is_sent", "updated_at"]
                            )
                        )
                        # ---

                        log.info(log_t + "# The second letter is gone")

                        # ---
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

    from utilities.services import CustomizationSyncAsyncLoop

    log_t = "[task_postman]:"
    try:
        log.info(log_t + " start.")
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
