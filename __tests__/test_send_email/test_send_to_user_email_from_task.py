"""
__tests__/test_send_email/test_send_to_user_email_from_task.py:1
"""
import json
import logging
import queue
import re
from typing import Any, Mapping, Optional, Union

from __tests__.fixtures.fixture_django import pytest_generate_tests
from __tests__.fixtures.fixture_mock_patch import (
    mock_cacher_adapter_mixin,
    mock_subPerson_class,
)
from persons.interfaces import UsersPydantic

log = logging.getLogger(__name__)




class TestSendToUserEmailFromTask:

    async def test_send_letter_to_user_email(self, mock_cacher_adapter_mixin,
                                             users_model_data, mocker):
        """
        Here is a goal to send a latter and say about registration.
        First letter will say about: "Your email address was used for registration the new account "
        :return:
        """


        import queue

        from persons import EnumTemplatesKeysCache
        from persons.adapters import PostmanAdapter
        from persons.tasks.sub_tasks_celery.sub_task_get_send_letter import (
            child_process_emailing,
        )
        from persons.tasks.tasks_celery.task_send_letter_to_user_email import (
            child_process_get_keys_0,
            send_letter_to_user_email,
        )
        log_t = "[TestSendToUserEmailFromTask][test_send_letter_to_user_email]:"
        test_keys_queue = queue.Queue(2000)
        # ----
        log.info("""\n
        # ============================================
        # Mock the person_database_adapter.py::PersonServiceDatabaseAdapter.get_user_by_email()
        # and
        # Mock the person_database_adapter.py::PersonServiceDatabaseAdapter.create_or_update_in_database()
        # ============================================
        """)
        mock_get_user_by_email = mocker.patch(
            "persons.adapters.person_database_adapter.PersonServiceDatabaseAdapter.get_user_by_email")
        user_object = UsersPydantic(**users_model_data)
        mock_get_user_by_email.return_value = user_object
        # ----
        mock_create_or_update_in_database = mocker.patch(
            "persons.adapters.person_database_adapter.PersonServiceDatabaseAdapter.create_or_update_in_database")

        mock_create_or_update_in_database.side_effect = lambda user_data=None: None

        # ----
        log.info("""\n
        # ============================================
        # Mock  task_send_letter_to_user_email.py::child_process_get_keys_0
        # ============================================
        """)
        mock_child_process_get_keys_0 = mocker.patch(
            "persons.tasks.tasks_celery.task_send_letter_to_user_email.child_process_get_keys_0")
        mock_child_process_get_keys_0.side_effect = lambda key_pattern,\
                                                           log_t,\
                                                           queue: True

        # ----
        # if users_model_data["id"] == 10:
        bytes_Line = json.dumps({"username": users_model_data["username"], "email": users_model_data["email"]}).encode()
        test_keys_queue.put_nowait(bytes_Line)
        log.info("""\n
        # ============================================
        # Mock the task_send_letter_to_user_email.py::sub_function()
        # ============================================
        """)
        mock_sub_function = mocker.patch("persons.tasks.tasks_celery.task_send_letter_to_user_email.sub_function")
        # ============================================
        # Test tHe task_send_letter_to_user_email.py::send_letter_to_user_email
        # This task have two letters.
        # 1. First letter only take was - your email address was used as login
        # for the opening new account.
        # and
        # 2. Second letter need to send the code verification.
        # ============================================
        def sub_function(
            keys_queue: queue,
            log_t: str,
            result_bool: bool,
            subject_: str,
            text_context_: str,
            context_: Optional[Mapping[str, Any]],
        ) -> list | bool:
            """
            :param queue keys_queue: Required.
            :param str log_t: Required. It is a prefix for the logs.
            :param result_bool: Required.
            :param str subject_: Required. It is thema/heading for a letter.
            :param str text_context_: Required. It is massage in the letter body
            :param Optional[Mapping[str, Any]] context_: It is acontext data from the letter body.
            :return:
            """
            log.info(f"""\n
            # ============================================
            # Start the task_send_letter_to_user_email.py::sub_function()
            # keys_queue: {str(keys_queue)} & Type: {type(keys_queue)},
            # log_t: {str(log_t)} & Type: {type(log_t)},
            # result_bool: {str(result_bool)} & Type: {type(result_bool)},
            # subject_: {str(subject_)} & Type: {type(subject_)},
            # text_context_: {str(text_context_)} & Type: {type(text_context_)},
            # context_: {str(context_)} & Type: {type(context_)},,
            # ============================================
            """)
            list_of_results = []
            keys_queue: queue = test_keys_queue
            log_t = log_t[:-1] + "[test sub_function]:"
            result_bool = True
            qsize = keys_queue.qsize()
            if result_bool and qsize:
                while not keys_queue.empty():
                    byte_code = keys_queue.get_nowait()
                    json_code = json.loads(byte_code.decode("utf-8"))
                    list_of_results.append(json_code)
            else:
                return False
            # The clean storage
            del qsize
            if len(list_of_results) == 0:
                log.warning(
                    log_t
                    + " Queue empty. Maybe what wrong! Length of list: %s "
                    % len(list_of_results)
                )
                return False
            kwargs = {"subject": subject_, "text_context": text_context_, "contex": context_}
            result_bool = child_process_emailing(*(list_of_results,), **kwargs)
            assert isinstance(result_bool, bool)
            assert result_bool

            return list_of_results

        mock_sub_function.side_effect = sub_function

        # ----
        email = users_model_data["email"]
        kwargs = {"username": users_model_data["username"], "email": email}
        # ----

        mock_subperson__get_cache = mocker.patch(
            "persons.adapters.postman_adapter.PostmanAdapter.SubPerson._SubPerson__get_cache")
        mock_subperson__get_cache.return_value = [json.dumps([kwargs,]).encode()]
        # ----
        log.info("""\n
        # ============================================
        # TEST THE send_letter_to_user_email() BEGINNING
        # ============================================
        """)

        args = (EnumTemplatesKeysCache.USER_PENDING.value % re.sub(r"[@.]", "", email),)
        test_send_letter_to_user_email = await send_letter_to_user_email(*args, *kwargs)

        # ----
        assert isinstance(test_send_letter_to_user_email, bool|list)
        assert test_send_letter_to_user_email

        mock_get_user_by_email.assert_called()

        mock_sub_function.assert_called()


        mock_child_process_get_keys_0.assert_called()


        mock_create_or_update_in_database.assert_called()
