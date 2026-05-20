"""
__test__/test_caching/test_cache_manager_saving.py:1
"""

import logging

import pytest
from pydantic import EmailStr

from __tests__.fixtures.fixture_django import django_setup, mock_pydantic_user
from persons.interfaces import EmailString

log = logging.getLogger(__name__)


@pytest.mark.usefixtures("django_setup")
class TestCacheManagerSaving:

    @pytest.mark.parametrize(
        "key_str, data_dict, expected",
        [
            (
                "user:pending:letter_1:%s" % "test_mailhostru",
                {"email": "test_mail@host.ru", "username": "SergeyTest"},
                True,
            ),
            (
                "user:pending:letter_1:%s" % "test_2_mailhostru",
                {"email": "test_2_mail@host.ru", "username": "SergeyTest"},
                True,
            ),
        ],
    )
    async def test_cache_manager_method_save(self, key_str, data_dict, expected):
        from persons.services.caching import CacheManager

        log.info("\n 1. До создания CacheManager")
        cachemanager = CacheManager()
        log.info(" 2. После создания CacheManager")
        log.info(" 3. Перед asynccacher.asave()")
        result_bool = await cachemanager.asave(key_str, data_dict)
        assert isinstance(result_bool, bool)
        assert result_bool == expected
        log.info(f" 4. После asynccacher.asave() = {result_bool}")

    @pytest.mark.parametrize(
        "key_tuple, value_dict, expected",
        [
            (("user:pending:%s",), {}, True),
        ],
    )
    async def test_send_to_user_email(
        self,
        key_tuple,
        value_dict,
        expected,
    ):

        from persons.tasks.tasks_celery.task_send_letter_to_user_email import (
            send_letter_to_user_email,
        )

        log_t = "[test_send_to_user_email]:"
        # if not settings.configured:

        #     django.setup()
        # caplog.set_level(logging.INFO)
        log.info(
            log_t
            + " Key: %s & Value: %s"
            % (str(key_tuple[0] % "test_emailhoastru"), str(value_dict))
        )
        # for key in key_tuple:
        result_future = await send_letter_to_user_email(key_tuple[0], **value_dict)

        log.info(f"\n1. {log_t} Result type: {type(result_future)}")
        # print(f"2. [test test_send_to_user_email]:Result length: {len(result_future)}")

        # log.info(
        #     "3. [test test_send_to_user_email]: Context of result_list: %s"
        #     % str(result_future)
        # )
        # assert type(result_future) == dict
        # log.info(f"4. {log_t} Тип result_future: {type(result_future)}")
        assert result_future is not None
        assert result_future is expected

        # log.info(f"5. {log_t} Length result_future: {len(result_future)}")
        # k = list(result_future.keys())[0]
        # v = result_future.get(k)
        # log_t = (
        #     "[test test_send_to_user_email]: DEBUG  Key: %s Type KEY: %s Value: %s TYPE VALUE: %s"
        #     % (k, type(k), v, type(v))
        # )
        # log.info(log_t)
        # print("6. " + log_t)
        # assert "<Future" in str(v) and "list>" in str(v)
        # print("7. [test test_send_to_user_email]: DEBUG RESULT: %s" % v.result())
