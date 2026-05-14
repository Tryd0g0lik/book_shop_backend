"""
persons/adapters/cache_adapter.py:1
"""

import logging
import threading
from contextlib import contextmanager
from typing import Optional

from redis import ConnectionError, Redis, RedisError, TimeoutError

log = logging.getLogger(__name__)


class CacherAdapter:
    _pool = None
    __pool_lock = threading.Lock()

    def __init__(
        self,
        db: int = 0,
        max_connections: int = 20,
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
        self.__redis_password: Optional[str] = None
        self.__redis_db: int = db
        self.__redis_master_name: Optional[str] = None
        self.server_client: Optional[Redis] = None
        self.log_t = "[%s]:" % CacherAdapter.__class__.__name__

        self.max_connections: int = max_connections
        self.decode_responses: bool = decode_responses
        self.socket_connect_timeout: int = socket_connect_timeout
        self.socket_timeout: int = socket_timeout
        self.retry_on_timeout: bool = retry_on_timeout
        self.health_check_interval: int = health_check_interval

    def _init_pool(self) -> None:
        from redis.connection import ConnectionError, ConnectionPool

        from project.settings_conf.settings_env import (
            REDIS_HOST,
            REDIS_PORT,
        )

        try:
            if CacherAdapter._pool is None:
                with CacherAdapter.__pool_lock:
                    CacherAdapter._pool = ConnectionPool(
                        host=REDIS_HOST,
                        port=int(REDIS_PORT),
                        password=self.redis_password,
                        username=self.redis_master_name,
                        db=self.redis_database,
                        max_connections=self.max_connections,
                        decode_responses=self.decode_responses,
                        socket_connect_timeout=self.socket_connect_timeout,
                        socket_timeout=self.socket_timeout,
                        retry_on_timeout=self.retry_on_timeout,
                        health_check_interval=self.health_check_interval,
                    )
                    log.info(self.log_t + " Redis Connection pool initialized.")
        except Exception as e:
            log_t = self.log_t[
                :-1
            ] + " Connection with a cache server failed. %s" % str(e)
            raise ValueError(log_t)

    def __get_client(self):
        if CacherAdapter._pool is None:
            self._init_pool()
        return Redis(connection_pool=CacherAdapter._pool)

    def related(self) -> bool:
        if self.server_client is None:
            try:
                # ============================================
                # CONNECT TO THE CACHE SERVER
                # ============================================
                self.server_client = self.__get_client()
            except Exception as e:
                log_t = (
                    self.log_t
                    + " Connection with a cache server failed. %s" % e.args[0]
                    if e.args
                    else str(e)
                )
                raise ValueError(log_t)
        return True

    @contextmanager
    def connected(self):
        is_connected = self.is_connected
        if not is_connected:
            log_t = self.log_t + " Connection with a cache server is invalid."
            raise ValueError(log_t)
        # ============================================
        # GET REDIS CLIENT
        # ============================================
        server_client = self.server_client
        try:
            server_client.ping()
            yield server_client
        except ConnectionError as e:
            log_t = self.log_t[
                :-1
            ] + " ConnectionError. Connection with a cache server is closed.%s" % str(e)
            raise ConnectionError(log_t) from e

        except TimeoutError as e:
            log_t = self.log_t[
                :-1
            ] + " TimeoutError error. Connection with a cache server is closed.%s" % str(
                e
            )
            raise TimeoutError(log_t) from e

        except RedisError as e:
            log_t = self.log_t + "Mistake on a cache server: %s" % str(e)
            raise RedisError(log_t) from e

        except Exception as e:
            log_t = self.log_t + e.args[0] if e.args else str(e)
            raise ValueError(log_t)
        finally:
            pass

    def _recreated_pool(self):
        with CacherAdapter.__pool_lock:
            if CacherAdapter._pool:
                CacherAdapter._pool.disconnect()
                CacherAdapter._pool = None
            self._init_pool()

    def close(self):
        # ============================================
        # EVERY CONNECTION WILL BE CLOSED
        # ============================================
        is_connected = self.is_connected
        if is_connected:
            self.server_client = None
            CacherAdapter._pool = None

    @property
    def is_connected(self) -> bool:
        return True if CacherAdapter._pool is not None else False

    @property
    def redis_password(self) -> str:
        return self.__redis_password

    @redis_password.setter
    def redis_password(self, line: str) -> None:
        if isinstance(line, str) and len(line) == 0:
            log_t = self.log_t + " Password is invalid."
            raise ValueError(log_t)
        self.__redis_password = line

    @property
    def redis_master_name(self) -> str:
        return self.__redis_master_name

    @redis_master_name.setter
    def redis_master_name(self, line: str) -> None:
        if isinstance(line, str) and len(line) == 0:
            log_t = self.log_t + " User name is invalid."
            raise ValueError(log_t)
        self.__redis_master_name = line

    @property
    def redis_database(self) -> int:
        return self.__redis_db

    @redis_database.setter
    def redis_database(self, num: int) -> None:
        self.__redis_db = num
