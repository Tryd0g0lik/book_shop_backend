"""
persons/adapters/cache_base.py:1
"""

import re
from typing import Optional

from redis import Redis


class CacherBaseMixin:

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
        self.log_t = "[%s]:" % CacherBaseMixin.__class__.__name__

        self.max_connections: int = max_connections
        self.decode_responses: bool = decode_responses
        self.socket_connect_timeout: int = socket_connect_timeout
        self.socket_timeout: int = socket_timeout
        self.retry_on_timeout: bool = retry_on_timeout
        self.health_check_interval: int = health_check_interval

    @property
    def redis_password(self) -> str:
        return self._redis_password

    @redis_password.setter
    def redis_password(self, line: str) -> None:
        if line is not None or isinstance(line, str) and len(line) == 0:
            log_t = self.log_t + " Password is invalid."
            raise ValueError(log_t)
        self._redis_password = line

    @property
    def redis_master_name(self) -> str:
        return self._redis_master_name

    @redis_master_name.setter
    def redis_master_name(self, line: str) -> None:
        if (
            isinstance(line, str)
            and len(line) == 0
            and re.match(r"\w{1,50}", line, flags=re.ASCII)
        ):
            log_t = self.log_t + " User name is invalid."
            raise ValueError(log_t)
        self._redis_master_name = line

    @property
    def redis_database(self) -> int:
        return self._redis_db

    @redis_database.setter
    def redis_database(self, num: int) -> None:
        self._redis_db = num
