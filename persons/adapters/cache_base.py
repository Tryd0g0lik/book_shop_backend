"""
persons/adapters/cache_base.py:1
"""

from typing import Optional

from redis import Redis


class CacherBase:

    def __init__(
        self,
        db: int = 0,
        max_connections: int = 10,
        decode_responses: bool = False,
        socket_connect_timeout: int = 5,
        socket_timeout: int = 5,
        retry_on_timeout: bool = True,
        health_check_interval: int = 30,
    ) -> None:
        """
        This is the sync code.
        :param int db: This is integer nuber. That is number of the redis's db. Default value is 0.
        :param: Optional[str] redis_master_name. This is a string this is a name/login of the cache server. Default value is None.
        :param: Optional[str] redis_password. This is a string this is a password of the cache server. Default value is None.
        :param: method related. Connection with a cache server.
        :param: method closed. This method is close connection and assign 'self.server_caching = None'
        :param  connected has wrapper the contextmanager. Exemple: ```
            cache = CacheAdapter()
            cache.redis_password = "<PASSWORD>" # if required.
            cache.redis_master_name = "<LOGIN / USERNAME>" # if required.
            cache.related()
            try:
                with cache.connected() as conn:
                    # ...
            finally:
                cache.close()

        ```
        :param redis_master_name:
        """
        self._redis_password: Optional[str] = None
        self._redis_db: int = db
        self._redis_master_name: Optional[str] = None
        self.server_client: Optional[Redis] = None
        self.log_t = "[%s]:" % CacherBase.__class__.__name__

        self.max_connections: int = max_connections
        self.decode_responses: bool = decode_responses
        self.socket_connect_timeout: int = socket_connect_timeout
        self.socket_timeout: int = socket_timeout
        self.retry_on_timeout: bool = retry_on_timeout
        self.health_check_interval: int = health_check_interval
