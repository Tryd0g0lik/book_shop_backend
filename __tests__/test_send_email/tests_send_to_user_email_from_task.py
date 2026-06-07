# """
# __tests__/test_send_email/test_send_to_user_email_from_task.py:1
# """
# import json
# import logging
# import queue
# import re
# from typing import Any, Mapping, Optional, Union
# from unittest.mock import MagicMock
#
# import pytest
#
# from __tests__.fixtures.fixture_django import pytest_generate_tests
# from __tests__.fixtures.fixture_mock_patch import (
#     mock_cacher_adapter_mixin,
#     mock_subPerson_class,
# )
# from persons import EnumEmailLetter
# from persons.interfaces import UsersPydantic
# from persons.models import Users
#
# log = logging.getLogger(__name__)
#
#
#
#
# class TestSendToUserEmailFromTask:
#     @pytest.mark.skip()
#     @pytest.mark.django_db
#     async def test_send_letter_to_user_email(self, mock_cacher_adapter_mixin,
#                                              users_model_data, mocker):
#         """
#         Here is a goal to send the two latter for the avery user and say about registration.
#         First letter will say about: "Your email address was used for registration the new account "
#         :return:
#         """
#
#
#         import queue
#
#         from persons.tasks.tasks_celery.task_send_letter_to_user_email import (
#             child_process_get_keys_0,
#             send_letter_to_user_email,
#         )
#
#         # ----
#         log_t = "[TestSendToUserEmailFromTask][test_send_letter_to_user_email]:"
#         test_keys_queue = queue.Queue(2000)
#         # ----
#         log.info("""\n
#         # ============================================
#         # Mock the person_database_adapter.py::PersonServiceDatabaseAdapter.get_user_by_email()
#         # and
#         # Mock the person_database_adapter.py::PersonServiceDatabaseAdapter.create_or_update_in_database()
#         # ============================================
#         """)
#         mock_get_user_by_email = mocker.patch(
#             "persons.adapters.person_database_adapter.PersonServiceDatabaseAdapter.get_user_by_email")
#         mock_get_user_by_email.reset_mock()
#         user_object = Users(**users_model_data)
#         user_validation =  UsersPydantic.model_validate(user_object)
#         user_dict = UsersPydantic.to_dict_without_secret_data(user_validation)
#         mock_get_user_by_email.return_value = user_validation
#         # ----
#         mock_get_model = mocker.patch("persons.adapters.postman_adapter.PostmanAdapter.SubPerson.get_model")
#         mock_get_model.return_value = [user_dict]
#         # ----
#         log.info(f"""\n
#         # ============================================
#         # Mock the Users.object.update model of Persons model
#         # ============================================
# """)
#         # mock_update = mocker.MagicMock()
#         # mock_update.update.return_value = 1
#         mock_Users = mocker.patch("persons.models.Users")
#         mock_filter = MagicMock()
#         mock_filter.filter.return_value = [user_object]
#         mock_update = MagicMock()
#         mock_update.update.return_value = 1
#         mock_Users.filter.return_value = mock_filter
#         mock_Users.update.return_value = mock_update
#         # mock_filter.object.filter.return_value = lambda *args: 1
#         # mock_create_or_update_in_database = mocker.patch(
#         #     "persons.adapters.person_database_adapter.PersonServiceDatabaseAdapter.create_or_update_in_database")
#         # mock_create_or_update_in_database.reset_mock()
#         #
#         # def test_create_or_update_in_database(
#         #     user_data: dict,
#         #     user_id: Optional[int] = None,
#         #     user_email: Optional[str] = None,
#         # ):
#         #     return None
#         # mock_create_or_update_in_database.side_effect = test_create_or_update_in_database
#
#         # ----
#         log.info("""\n
#         # ============================================
#         # Mock  task_send_letter_to_user_email.py::child_process_get_keys_0
#         # ============================================
#         """)
#         mock_child_process_get_keys_0 = mocker.patch(
#             "persons.tasks.tasks_celery.task_send_letter_to_user_email.child_process_get_keys_0")
#         mock_child_process_get_keys_0.reset_mock()
#
#         bytes_Line = json.dumps(
#             {"username": users_model_data["username"], "email": users_model_data["email"]}).encode()
#         def mock_queue_collection(key_pattern, log_t, queue):
#
#             queue.put_nowait(bytes_Line)
#             return True
#
#         mock_child_process_get_keys_0.side_effect = mock_queue_collection
#
#         # ----
#         log.info("""\n
#         # ============================================
#         # Mock the task_send_letter_to_user_email.py::sub_function_send_mail()
#         # ============================================
#         """)
#         mock_sub_function = mocker.patch("persons.tasks.tasks_celery.task_send_letter_to_user_email.sub_function_send_mail")
#         mock_sub_function.reset_mock()
#         # ============================================
#         # Test tHe task_send_letter_to_user_email.py::send_letter_to_user_email
#         # This task have two letters.
#         # 1. First letter only take was - your email address was used as login
#         # for the opening new account.
#         # and
#         # 2. Second letter need to send the code verification.
#         # ============================================
#         def sub_function_send_mail(
#             list_of_keys: list,
#             log_t: str,
#             subject_: str,
#             text_context_: str,
#             context_: Optional[Mapping[str, Any]],
#         ) -> list | bool:
#             """
#             :param queue keys_queue: Required.
#             :param str log_t: Required. It is a prefix for the logs.
#             :param result_bool: Required.
#             :param str subject_: Required. It is thema/heading for a letter.
#             :param str text_context_: Required. It is massage in the letter body
#             :param Optional[Mapping[str, Any]] context_: It is acontext data from the letter body.
#             :return:
#             """
#             log_t = log_t[:-1] + "[test sub_function_send_mail]:"
#             log.info(f"""{log_t}\n
#             # ============================================
#             # Start the task_send_letter_to_user_email.py::sub_function_send_mail()
#             # list_of_keys: {str(list_of_keys)} & Type: {type(list_of_keys)},
#             # subject_: {str(subject_)} & Type: {type(subject_)},
#             # text_context_: {str(text_context_)} & Type: {type(text_context_)},
#             # context_: {str(context_)} & Type: {type(context_)},,
#             # ============================================
#             """)
#
#             # keys_queue: queue = test_keys_queue
#
#
#             kwargs = {"subject": subject_, "text_context": text_context_, "context": context_}
#             log.info(f"""{log_t}\n
#             # ============================================
#             # TEST BEFORE SEND LETTER child_process_emailing
#             # ============================================
#             # kwargs: {kwargs}
#             """)
#             result_bool = child_process_emailing(*(list_of_keys,), **kwargs)
#
#             assert isinstance(result_bool, bool)
#             assert result_bool
#
#             return list_of_keys
#
#         mock_sub_function.side_effect = sub_function_send_mail
#
#         # ----
#         log.info(f"""{log_t}\n
#         # ============================================
#         # TEST THE users_model_data DICT:
#         # ============================================
#         # users_model_data: {users_model_data}
#         """)
#
#         email = users_model_data["email"]
#         kwargs = {"username": users_model_data["username"], "email": email}
#         # ----
#
#         mock_subperson__get_cache = mocker.patch(
#             "persons.services.caching.CacheManager.aget")
#         mock_subperson__get_cache.reset_mock()
#         mock_subperson__get_cache.return_value = [json.dumps([kwargs,]).encode()]
#         # ----
#         log.info(f"""{log_t}\n
#         # ============================================
#         # TEST THE send_letter_to_user_email() BEGINNING
#         # ============================================
#         """)
#
#         # args = (EnumTemplatesKeysCache.USER_PENDING.value % re.sub(r"[@.]", "", email),)
#         test_send_letter_to_user_email = await send_letter_to_user_email()
#
#         # ----
#         assert isinstance(test_send_letter_to_user_email, bool|list)
#         assert test_send_letter_to_user_email
#
#
#
#         mock_sub_function.assert_called()
#         # This is simply logs
#         log.warning(mock_sub_function.call_args_list)
#         log.info(mock_sub_function.call_args_list[0])
#         log.info(mock_sub_function.call_args_list[0][0])
#         log.info(mock_sub_function.call_args_list[0].args)
#         log.info(mock_sub_function.call_args_list[0].kwargs)
#         log.info(mock_sub_function.mock_calls)
#
#
#         actual_call_args_first = mock_sub_function.call_args_list[0].args
#
#
#         assert actual_call_args_first[3] ==  EnumEmailLetter.CONFIRM_EMAIL_Letter_0.value
#         assert actual_call_args_first[-1] is None
#
#         actual_call_args_list_last = mock_sub_function.call_args_list[1].args
#         log.warning(f"--------------- \n {mock_sub_function.call_args_list[1]}" )
#         assert actual_call_args_list_last[-2] == EnumEmailLetter.CONFIRM_EMAIL_Letter_1.value
#
#         assert actual_call_args_list_last[-1] is not None
#         assert type(actual_call_args_list_last[-1]) == dict
#         assert len(actual_call_args_list_last[-1]["code"]) == 9
#         assert "{'user': " in str(actual_call_args_list_last[-1])
#         assert " 'code': " in str(actual_call_args_list_last[-1])
#
#
#         mock_child_process_get_keys_0.assert_called()
#
#
#         # mock_create_or_update_in_database.assert_called()
