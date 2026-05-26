"""
persons/adapters/cache_adapter.py:1
"""

import logging
import threading
from contextlib import contextmanager

from redis import AuthenticationError, ConnectionError, Redis, RedisError, TimeoutError

from .cache_base import CacherBaseMixin

# from typing import Optional


log = logging.getLogger(__name__)


class CacherAdapterMixin(CacherBaseMixin):
    _pool = None
    __pool_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        cls.log_t = "[%s]:" % CacherAdapterMixin.__class__.__name__
        return super().__new__(cls)

    def _init_pool(self) -> None:
        from redis.connection import ConnectionError, ConnectionPool

        from project.settings_conf.settings_env import (
            REDIS_HOST,
            REDIS_PORT,
        )

        try:
            if CacherAdapterMixin._pool is None:
                redis_database = self.redis_database
                redis_master_name = self.redis_master_name
                redis_password = self.redis_password
                with CacherAdapterMixin.__pool_lock:
                    CacherAdapterMixin._pool = ConnectionPool(
                        host=REDIS_HOST,
                        port=int(REDIS_PORT),
                        password=redis_password,
                        username=redis_master_name,
                        db=redis_database,
                        max_connections=self.max_connections,
                        decode_responses=self.decode_responses,
                        socket_connect_timeout=self.socket_connect_timeout,
                        socket_timeout=self.socket_timeout,
                        retry_on_timeout=self.retry_on_timeout,
                        health_check_interval=self.health_check_interval,
                    )
                    log.info(self.log_t + " Redis Connection pool initialized.")
        except ConnectionError as e:
            log_t = self.log_t + " %s" % str(e)
            raise ConnectionError(log_t) from e

        except Exception as e:
            log_t = self.log_t + " %s" % str(e)
            raise ValueError(log_t)

    def __get_client(self):
        if CacherAdapterMixin._pool is None:
            self._init_pool()
        return Redis(connection_pool=CacherAdapterMixin._pool)

    def related(self) -> bool:
        if self.server_client is None:
            try:
                # ============================================
                # CONNECT TO THE CACHE SERVER
                # ============================================
                self.server_client = self.__get_client()
            except Exception as e:
                log_t = self.log_t + " %s" % e.args[0] if e.args else str(e)
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
        except AuthenticationError as e:
            log_t = self.log_t[:-1] + " AuthenticationError error. %s" % str(
                e.args[0] if e.args else str(e)
            )
            raise AuthenticationError(log_t) from e

        except RedisError as e:
            log_t = self.log_t + "Mistake on a cache server: %s" % str(e)
            raise RedisError(log_t) from e

        except Exception as e:
            log_t = self.log_t + e.args[0] if e.args else str(e)
            raise ValueError(log_t)
        finally:
            pass

    def _recreated_pool(self):
        with CacherAdapterMixin.__pool_lock:
            if CacherAdapterMixin._pool:
                CacherAdapterMixin._pool.disconnect()
                CacherAdapterMixin._pool = None
            self._init_pool()

    def close(self):
        # ============================================
        # EVERY CONNECTION WILL BE CLOSED
        # ============================================
        is_connected = self.is_connected
        if is_connected:
            self.server_client = None
            CacherAdapterMixin._pool = None

    @property
    def is_connected(self) -> bool:
        return True if CacherAdapterMixin._pool is not None else False
