"""
__test__/test_caching/test_cache_manager_saving.py:1
"""

import logging

import django
import pytest
from django.conf import settings

from __tests__.fixtures.fixture_django import django_setup
from __tests__.fixtures.fixture_pydantic import mock_pydantic_user

log = logging.getLogger(__name__)
log.info("""
# ============================================
# __test__/test_caching/test_cache_manager_saving.py:1
# ============================================
""")

@pytest.mark.usefixtures("django_setup")
class TestCacheManagerSaving:

    @pytest.mark.parametrize(
        "key_str, data_dict, expected",
        [
            (
                "user:pending:letter:%s" % "test_mailhostru",
                {"email": "test_mail@host.ru", "username": "SergeyTest"},
                True,
            ),
            (
                "user:pending:letter:%s" % "test_2_mailhostru",
                {"email": "test_2_mail@host.ru", "username": "SergeyTest"},
                True,
            ),
        ],
    )
    async def test_cache_manager_method_save(self, key_str, data_dict, expected):
        from persons.services import CacheManager

        cachemanager = CacheManager()
        result_bool = await cachemanager.asave(key_str, data_dict)
        assert isinstance(result_bool, bool)
        assert result_bool == expected
