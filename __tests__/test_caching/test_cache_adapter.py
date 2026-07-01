""" "
 __tests__/test_caching/test_cache_adapter.py:1

Redis's option by default are:
- db: int = 0,
- max_connections: int = 10,
- decode_responses: bool = False,
- socket_connect_timeout: int = 5,
- socket_timeout: int = 5,
- retry_on_timeout: bool = True,
- health_check_interval: int = 30,
"""

from threading import Thread
from unittest.mock import MagicMock

import pytest
import redis
from pytest_mock import mocker

from __tests__.test_caching.fixture_caching import fixture_cacher_adapter_mixin

REDIS_DB = 2


class TestCacherAdapter:

    def test_init_pool(self, fixture_cacher_adapter_mixin, mocker):
        """
        Uor goal is checking the pool and threading. How will a loop behave when will be having
            more initialize the ConnectionPool. That we don't have real the Redis's call
        :return: We must have only one collection of workers created
        """

        test_cacher = fixture_cacher_adapter_mixin
        mock_pool = mocker.patch("redis.connection.ConnectionPool")
        mock_pool.return_value = "SUCCESS"

        mock_pool.reset_mock()

        def _test_init_pool():
            test_cacher._init_pool()

        test_threads = []
        for _ in range(10):
            test_thread = Thread(target=_test_init_pool)
            test_threads.append(test_thread)
            test_thread.start()

        # [for tth in test_threads]
        for tth in test_threads:
            tth.join()
        mock_pool.assert_called_once()
        assert fixture_cacher_adapter_mixin._pool
        assert fixture_cacher_adapter_mixin._pool == "SUCCESS"

    def test_related(self, fixture_cacher_adapter_mixin, mocker):
        """
        Our goal is checking the answer from the 'CacherAdapter.related'.
        Thy are mocks:
            - CacherAdapter.__get_client
        :param mocker:
        :param fixture_cacher_adapter_mixin: This is running the CacherAdapter().
        '''
            test_cacher = CacherAdapter()
            CacherAdapter._pool = None
            yield test_cacher
            if test_cacher.is_connected:
            test_cacher.close()
        '''
        :return: We must get only one call or mistake.
        """
        test_cacher = fixture_cacher_adapter_mixin

        mock__get_client = mocker.patch.object(
            fixture_cacher_adapter_mixin, "_CacherAdapter__get_client"
        )
        mock__get_client.return_value = "SUCCESS"
        assert test_cacher.server_client is None
        test__result = test_cacher.related()
        assert isinstance(test_cacher.server_client, str)
        assert test_cacher.server_client == "SUCCESS"
        assert test__result is True
        assert test__result

    def test_ping_of_connected(self, fixture_cacher_adapter_mixin, mocker):
        """
        HEre is we have a real conaction with the redis's server.
        Our goal - it get the error response when we have a mistake to the '.ping()'
        :param fixture_cacher_adapter_mixin:
        :param mocker:
        :return:
        """
        from redis import ConnectionError

        test_cacher = fixture_cacher_adapter_mixin

        mocker.patch(
            "persons.adapters.CacherAdapter.is_connected",
            new_callable=mocker.PropertyMock,
            return_value=True,
        )
        mock_client = MagicMock()
        mock_client.ping.side_effect = ConnectionError()
        test_cacher.server_client = mock_client

        with pytest.raises(ConnectionError) as exc_resp:

            with test_cacher.connected():
                pass
        assert "ConnectionError. Connection with a cache server is closed" in str(
            exc_resp.value
        )
        mock_client.ping.assert_called()
