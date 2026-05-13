"""
__test__/test_send_email/test_send_to_user_email.py:1
"""

import asyncio
import logging

import pytest

from persons.tasks.tasks_celery.task_send_letter_to_user_email import (
    send_letter_to_user_email,
)

log = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "key_tuple, value_dict, expected",
    [
        (("user:pending:*",), {}, False),
    ],
)
async def test_send_to_user_email(key_tuple, value_dict, expected, caplog):
    caplog.set_level(logging.INFO)
    log.info(
        "[test test_send_to_user_email]: Key: %s & Value: %s"
        % (str(key_tuple), str(value_dict))
    )
    result_future = await send_letter_to_user_email(key_tuple, **value_dict)
    print(f"\n[test test_send_to_user_email]: Result type: {type(result_future)}")
    print(f"[test test_send_to_user_email]:Result length: {len(result_future)}")
    log.info(
        "[test test_send_to_user_email]: Context of result_list: %s"
        % str(result_future)
    )
    assert type(result_future) == dict
    assert len(result_future) > 0
    k = list(result_future.keys())[0]
    v = result_future.get(k)
    print(f"Тип result: {type(v)}")
    print(f"Is Future: {isinstance(v, asyncio.Future)}")
    print(f"Is Task: {isinstance(v, asyncio.Task)}")
    print(f"asyncio.isfuture: {asyncio.isfuture(v)}")
    log.info("[test test_send_to_user_email]: DEBUG TYPE VALUE: %s" % v)
    assert "<Future" in str(v) and "list>" in str(v)
    print("[test test_send_to_user_email]: DEBUG RESULT: %s" % v.result())
