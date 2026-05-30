# __tests__/test_tasks/test_cache_user_data.py:1

import logging

import pytest

log = logging.getLogger(__name__)

class TestCacheUserData:
    """
    This test for testing the 'cache_user_data' function from 'persons/tasks/tasks_celery/task_cache_user_email_before_verification.py:1'.
    Was tested the different These are templates from the 'persons.__init__:EnumTemplatesREGEX.PERSON_KEYS_OF_CACHE_IN_REGEX'
    """

    @pytest.mark.parametrize("args, qwargs, expected", [
        (('user:pending:work80mailry',), {'username': 'Sergey', 'email': 'work80@mail.ry'}, True),
        (('user:pending:work@80mailry',), {'username': 'Sergey', 'email': 'work80@mail.ry'}, False),
        (('user:pending:work80mail.ry',), {'username': 'Sergey', 'email': 'work80@mail.ry'}, False),
        (('user:pending:letter:work80mailry',), {'username': 'Sergey', 'email': 'work80@mail.ry'}, True),
    ])
    async def test_cache_user_data(self, args, qwargs, expected):
        from persons.tasks.tasks_celery.task_set_cache import cache_user_data
        result_bool = await cache_user_data(*args, **qwargs)
        assert result_bool == expected
