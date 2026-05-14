"""
__test__/test_caching/test_cache_manager_saving.py:1
"""

import logging

import pytest

from persons.services.caching import CacheManager


@pytest.mark.parametrize(
    "key_str, data_dict, expected",
    [
        (
            "user:pending:test_mailhostru",
            {"email": "test_mail@host.ru", "username": "SergeyTest"},
            True,
        ),
    ],
)
async def test_cache_manager_method_save(key_str, data_dict, expected):
    print("\n 1. До создания CacheManager")
    cachemanager = CacheManager()
    print(" 2. После создания CacheManager")
    print(" 3. Перед asynccacher.asave()")
    result_bool = await cachemanager.asave(key_str, data_dict)
    assert isinstance(result_bool, bool)
    assert result_bool == expected
    print(f" 4. После asynccacher.asave() = {result_bool}")
