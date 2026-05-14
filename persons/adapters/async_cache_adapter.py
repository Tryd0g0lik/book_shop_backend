"""
persons/adapters/async_cache_adapter.py:1
"""

import asyncio
import logging
import re
from contextlib import asynccontextmanager
from typing import Optional

from redis.asyncio import ConnectionError as AsyncConnectionError
from redis.asyncio import Redis, RedisError
from redis.asyncio.connection import ConnectionPool

from persons.adapters.cache_base import CacherBase

log = logging.getLogger(__name__)


class AsyncCacherAdapter(CacherBase):

    async_pool: Optional[ConnectionPool] = None

    def __init__(
        self,
        db: int = 0,
        max_connections: int = 10,
        decode_responses: bool = False,
        socket_connect_timeout: int = 5,
        socket_timeout: int = 5,
        retry_on_timeout: bool = True,
        health_check_interval: int = 30,
    ):
        super().__init__(
            db,
            max_connections,
            decode_responses,
            socket_connect_timeout,
            socket_timeout,
            retry_on_timeout,
            health_check_interval,
        )
        self.log_t = "[AsyncCacherAdapter]:"
        self.async_lock = asyncio.Lock()

    async def _init_pool(self) -> None:

        from project.settings_conf.settings_env import (
            REDIS_HOST,
            REDIS_PORT,
        )

        try:
            if AsyncCacherAdapter.async_pool is None:
                # ============================================
                # GET WORKERS
                # ============================================
                log.info(
                    self.log_t
                    + self._init_pool.__name__
                    + " Before Redis Connection & pool initialized."
                )
                print(
                    self.log_t
                    + self._init_pool.__name__
                    + " Before Redis Connection & pool initialized."
                )
                # async with self.async_lock:
                print(
                    self.log_t
                    + self._init_pool.__name__
                    + " Before the async pool initialized."
                )
                AsyncCacherAdapter.async_pool = ConnectionPool(
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
                log.info(
                    self.log_t
                    + self._init_pool.__name__
                    + " Redis Connection pool initialized."
                )
                print(
                    self.log_t
                    + self._init_pool.__name__
                    + " Redis Connection pool initialized."
                )
        except Exception as e:
            log_t = (
                self.log_t[:-1]
                + self._init_pool.__name__
                + " Connection with a cache server failed. %s" % str(e)
            )
            print(log_t)
            raise ValueError(log_t)

    async def _get_client(self):
        if AsyncCacherAdapter.async_pool is None:
            async with self.async_lock:
                await self._init_pool()
        return Redis(connection_pool=AsyncCacherAdapter.async_pool)

    async def related(self) -> bool:
        if self.server_client is None:
            try:
                # ============================================
                # CONNECT TO THE CACHE SERVER
                # ============================================
                self.server_client = await self._get_client()
            except Exception as e:
                log_t = self.log_t if e.args else str(e) + self.related.__name__
                log_t += (
                    self.related.__name__
                    + " Connection with a cache server failed. %s" % e.args[0]
                )
                print(log_t)
                raise ValueError(log_t)
        return True

    @asynccontextmanager
    async def asyncconnected(self):
        is_connected = await self.is_connected()
        if not is_connected:
            log_t = self.log_t + " Connection with a cache server is invalid."
            await self._recreated_pool()
            raise ValueError(log_t)
        # ============================================
        # GET REDIS CLIENT
        # ============================================
        server_client = self.server_client
        if server_client is None:
            raise ValueError(self.log_t + " Server client not initialized")
        try:
            await server_client.ping()
            yield server_client
        except AsyncConnectionError as e:
            log_t = self.log_t[
                :-1
            ] + " AsyncConnectionError. Connection with a cache server is closed.%s" % str(
                e
            )
            await self._recreated_pool()
            raise AsyncConnectionError(log_t) from e

        except TimeoutError as e:
            log_t = self.log_t[
                :-1
            ] + " TimeoutError error. Connection with a cache server is closed.%s" % str(
                e
            )
            raise TimeoutError(log_t) from e
        except RedisError as e:
            log_t = self.log_t + "Mistake on a cache server: %s" % str(e)
            await self._recreated_pool()
            raise RedisError(log_t) from e

        except Exception as e:
            log_t = self.log_t + e.args[0] if e.args else str(e)
            await self._recreated_pool()
            raise ValueError(log_t)
        finally:
            pass

    async def _recreated_pool(self):
        async with self.async_lock:
            is_pool = AsyncCacherAdapter.async_pool
            if is_pool is not None:
                await AsyncCacherAdapter.async_pool.disconnect()
                AsyncCacherAdapter.async_pool = None
            await self._init_pool()

    async def close(self):
        # ============================================
        # EVERY CONNECTION WILL BE CLOSED
        # ============================================

        if self.server_client:
            await self.server_client.close()
            self.server_client = None
        is_pool = AsyncCacherAdapter.async_pool
        if is_pool is not None:
            await AsyncCacherAdapter.async_pool.disconnect()
            AsyncCacherAdapter.async_pool = None

    async def is_connected(self) -> bool:
        is_pool = AsyncCacherAdapter.async_pool
        if is_pool is None:
            return False
        try:
            client = self.server_client
            if client is None or not client:
                return False

            await client.ping()
            return True
        except AsyncConnectionError as e:
            log.error(
                AsyncConnectionError(
                    self.log_t
                    + " Connection with a cache server is invalid. AsyncConnectionError: %s"
                    % e.args[0]
                    if e.args
                    else str(e)
                )
            )
            return False
        except TimeoutError as e:
            log.error(
                TimeoutError(
                    self.log_t
                    + " Connection with a cache server is invalid. TimeoutError: %s"
                    % e.args[0]
                    if e.args
                    else str(e)
                )
            )
            return False
        except RedisError as e:
            log.error(
                RedisError(
                    self.log_t
                    + " Connection with a cache server is invalid. RedisError: %s"
                    % e.args[0]
                    if e.args
                    else str(e)
                )
            )
            return False
        except Exception as e:
            log.error(
                self.log_t
                + " Connection with a cache server failed. %s"
                % str(e.args[0] if e.args else str(e))
            )
            return False

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
