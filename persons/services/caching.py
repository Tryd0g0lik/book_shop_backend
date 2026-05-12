"""
persons/adapters/caching.py:2
"""

import logging
from contextlib import contextmanager
from typing import Optional

from redis import ConnectionError, Redis, RedisError, TimeoutError

log = logging.getLogger(__name__)


class Cacher:
    def __init__(
        self,
        db: int = 0,
    ) -> None:
        """
        This is the sync code.
        :param int db: This is integer nuber. That is number of the redis's db. Default value is 0.
        :param: Optional[str] master_name. This is a string this is a name/login of the cache server. Default value is None.
        :param: Optional[str] db_password. This is a string this is a password of the cache server. Default value is None.
        :param: method related. Connection with a cache server.
        :param: method closed. This method is close connection and assign 'self.server_caching = None'
        :param  connected has wrapper the contextmanager. Exemple: ```
            cache = CacheAdapter()
            cache.db_password = "<PASSWORD>" # if required.
            cache.master_name = "<LOGIN / USERNAME>" # if required.
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
        self.server_caching: Optional[Redis] = None
        self.log_t = "[%s]:" % Cacher.__class__.__name__

    def related(self) -> None:
        from project.settings_conf.settings_env import (
            REDIS_HOST,
            REDIS_PORT,
        )

        _redis_master_name = self.master_name
        _db_password = self.db_password
        self.server_caching = Redis(
            host=REDIS_HOST,
            port=int(REDIS_PORT),
            password=_db_password,
            username=_redis_master_name,
            db=self.__redis_db,
        )

    @contextmanager
    def connected(self):
        is_connected = self.is_connected
        if not is_connected:
            log_t = self.log_t + " Connection with a cache server is invalid."
            raise ValueError(log_t)
        server_cache = self.server_caching
        try:
            yield server_cache
        except TimeoutError as e:
            log_t = self.log_t + " Connection with a cache server timed out. %s" % str(
                e
            )
            raise TimeoutError(log_t)

        except RedisError as e:
            log_t = self.log_t + "Mistake on a cache server: %s" % str(e)
            raise ValueError(log_t)
        except Exception as e:
            log_t = self.log_t + e.args[0] if e.args else str(e)
            raise ValueError(log_t)
        finally:
            self.close()
            log_t = self.log_t + " Connection with a cache server is closed."
            log.info(log_t)

    def close(self):
        is_connected = self.is_connected
        if is_connected:
            self.server_caching = None

    @property
    def is_connected(self) -> bool:
        return True if self.server_caching is not None else False

    @property
    def db_password(self) -> str:
        return self.__redis_password

    @db_password.setter
    def db_password(self, line: str) -> None:
        if isinstance(line, str) and len(line) == 0:
            log_t = self.log_t + " Password is invalid."
            raise ValueError(log_t)
        self.__redis_password = line

    @property
    def master_name(self) -> str:
        return self.__redis_master_name

    @master_name.setter
    def master_name(self, line: str) -> None:
        if isinstance(line, str) and len(line) == 0:
            log_t = self.log_t + " User name is invalid."
            raise ValueError(log_t)
        self.__redis_master_name = line
