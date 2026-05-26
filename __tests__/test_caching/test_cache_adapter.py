""""
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

REDIS_DB = 2

class TestCacherAdapterMixin:

    def test_init_pool(self, mocker):
        """
        Uor goal is checking the pool and threading. How will a loop behave when will be having
            more initialize the ConnectionPool. That we don't have real the Redis's call
        :return: We must have only one collection of workers created
        """
        from persons.adapters import CacherAdapterMixin


        mock_pool = mocker.patch("redis.connection.ConnectionPool")
        mock_pool.return_value = "SUCCESS"

        test_cacher = CacherAdapterMixin()
        CacherAdapterMixin._pool = None
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
        assert CacherAdapterMixin._pool
        assert CacherAdapterMixin._pool == "SUCCESS"
