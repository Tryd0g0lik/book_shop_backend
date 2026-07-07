"""
__test__/test_caching/test_cache_manager_saving.py:1
"""

import asyncio
import logging
import queue

import pytest

from __tests__.fixtures.fixture_django import django_setup

log = logging.getLogger(__name__)
log.info("""
# ============================================
# __test__/test_caching/test_cache_manager_saving.py:1
# ============================================
""")


@pytest.mark.usefixtures("django_setup")
class TestCacheManager:

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
        from utilities.services import CacheManager

        cachemanager = CacheManager()
        result_bool = await cachemanager.asave(key_str, data_dict)
        assert isinstance(result_bool, bool)
        assert result_bool == expected

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
    async def test_cache_manager_method_aget(self, key_str, data_dict, expected):
        """
        Checking the condition 'persons/services/caching.py:232'
        :param key_str:
        :param data_dict:
        :param expected:
        :return:
        """
        from utilities.services import CacheManager

        queue_ = queue.Queue()
        cachemanager = CacheManager()
        result_bool = await cachemanager.asave(key_str, data_dict)
        assert isinstance(result_bool, bool)
        assert result_bool == expected
        result_bool = await cachemanager.aget(key=key_str, queue_collection=queue_)
        assert result_bool == expected
        assert queue_.qsize() == 1
        log.info(f"[test_cache_manager_method_aget]: qsize:{queue_.qsize()}")
        bytes_bytest = queue_.get_nowait()
        log.info(f"[test_cache_manager_method_aget]: bytes_list:{bytes_bytest}")
        assert isinstance(bytes_bytest, bytes)

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
    async def test_cache_manager_method_aget(self, key_str, data_dict, expected):
        """
        Checking the condition: 'persons/services/caching.py:361'
        :param key_str:
        :param data_dict:
        :param expected:
        :return:
        """
        from utilities.services import CacheManager

        collections_ = []
        cachemanager = CacheManager()
        result_bool = await cachemanager.asave(key_str, data_dict)
        assert isinstance(result_bool, bool)
        assert result_bool == expected
        result_bool = await cachemanager.aget(key=key_str, collection=collections_)
        assert result_bool == expected
        assert len(collections_) == 1
        log.info(f"[test_cache_manager_method_aget]: Len:{len(collections_)}")

        assert isinstance(collections_[0], bytes)

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
    async def test_cache_manager_method_aget(self, key_str, data_dict, expected):
        """
        Checking the condition: 'persons/services/caching.py:335'
        :param key_str:
        :param data_dict:
        :param expected:
        :return:
        """
        from utilities.services import CacheManager

        collections_ = []
        cachemanager = CacheManager()
        result_bool = await cachemanager.asave(key_str, data_dict)
        assert isinstance(result_bool, bool)
        assert result_bool == expected
        result_bool = await cachemanager.aget(
            key=key_str, collection=collections_, exat=1
        )
        assert result_bool == expected
        assert len(collections_) == 1
        log.info(f"[test_cache_manager_method_aget]: Len:{len(collections_)}")

        assert isinstance(collections_[0], bytes)
        await asyncio.sleep(1)
        result_bool = await cachemanager.aget(
            key=key_str, collection=collections_, exat=1
        )
        log.info(f"[test_cache_manager_method_aget]: result_bool:{result_bool}")

        assert result_bool is None

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
    async def test_cache_manager_method_aget(self, key_str, data_dict, expected):
        """
        Checking the condition: 'persons/services/caching.py:335'
        :param key_str:
        :param data_dict:
        :param expected:
        :return:
        """
        from utilities.services import CacheManager

        queue_ = queue.Queue()
        cachemanager = CacheManager()
        result_bool = await cachemanager.asave(key_str, data_dict)
        assert isinstance(result_bool, bool)
        assert result_bool == expected
        result_bool = await cachemanager.aget(
            key=key_str, queue_collection=queue_, exat=1
        )
        assert result_bool == expected
        assert queue_.qsize() == 1
        log.info(f"[test_cache_manager_method_aget]: qsize:{queue_.qsize()}")
        collections_ = queue_.get_nowait()
        assert isinstance(collections_, bytes)
        await asyncio.sleep(1)
        result_bool = await cachemanager.aget(
            key=key_str, queue_collection=queue_, exat=1
        )
        log.info(f"[test_cache_manager_method_aget]: result_bool:{result_bool}")

        assert result_bool is None
