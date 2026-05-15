# """
# __test__/test_send_email/test_send_to_user_email.py:1
# """
#
# # import asyncio
# import logging
#
# import pytest
#
# # from isort.profiles import django
# #
# # from project import settings
#
# # from persons import EnumTemplatesKeysCache
#
#
# log = logging.getLogger(__name__)
#
#
# @pytest.mark.parametrize(
#     "key_tuple, value_dict, expected",
#     [
#         (("user:pending:%s",), {}, False),
#     ],
# )
# @pytest.mark.order(2)
# async def test_send_to_user_email(
#     key_tuple,
#     value_dict,
#     expected,
# ):
#     import os
#
#     from persons.tasks.tasks_celery.task_send_letter_to_user_email import (
#         send_letter_to_user_email,
#     )
#     from project import settings
#
#     log_t = f"[{test_send_to_user_email.__name__}]:"
#     # if not settings.configured:
#     # if not settings:
#     #     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
#     #     django.setup()
#     # caplog.set_level(logging.INFO)
#     log.info(
#         "[test test_send_to_user_email]: Key: %s & Value: %s"
#         % (str(key_tuple[0] % "test_emailhoastru"), str(value_dict))
#     )
#     print(
#         "0. [test test_send_to_user_email]: Key: %s & Value: %s"
#         % (str(key_tuple[0] % "test_emailhoastru"), str(value_dict))
#     )
#     # for key in key_tuple:
#     result_future = await send_letter_to_user_email(key_tuple[0], **value_dict)
#
#     log.warning(
#         f"\n1. [test test_send_to_user_email]: Result type: {type(result_future)}"
#     )
#     # print(f"2. [test test_send_to_user_email]:Result length: {len(result_future)}")
#     log.info(
#         "[test test_send_to_user_email]: Context of result_list: %s"
#         % str(result_future)
#     )
#     print(
#         "3. [test test_send_to_user_email]: Context of result_list: %s"
#         % str(result_future)
#     )
#     assert type(result_future) == dict
#     print(f"4. {log_t} Тип result_future: {type(result_future)}")
#     assert len(result_future) > 0
#     print(f"5. {log_t} Length result_future: {len(result_future)}")
#     k = list(result_future.keys())[0]
#     v = result_future.get(k)
#     log_t = (
#         "[test test_send_to_user_email]: DEBUG  Key: %s Type KEY: %s Value: %s TYPE VALUE: %s"
#         % (k, type(k), v, type(v))
#     )
#     log.info(log_t)
#     print("6. " + log_t)
#     assert "<Future" in str(v) and "list>" in str(v)
#     print("7. [test test_send_to_user_email]: DEBUG RESULT: %s" % v.result())
