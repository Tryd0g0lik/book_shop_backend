# persons/interfaces/interface_cache_adapter.py:3

from contextlib import asynccontextmanager, contextmanager
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Protocol, Union

if TYPE_CHECKING:
    import queue
    import threading

    from redis import Redis, connection
    from redis.asyncio import Redis as AsyncRedis
    from redis.asyncio import connection as asyncConnection

    from persons.interfaces import UsersPydantic


class CacherBaseMixin(Protocol):

    @property
    def redis_password(self) -> str: ...

    @property
    def redis_master_name(self) -> str: ...

    @property
    def redis_database(self) -> int: ...


class AsyncCacherAdapter(CacherBaseMixin, Protocol):
    async_pool: ClassVar[
        Union["connection.ConnectionPool", "asyncConnection.ConnectionPool"]
    ]

    async def _init_pool(self) -> None: ...

    async def _get_client(self) -> "AsyncRedis": ...

    async def related(self) -> bool: ...

    @asynccontextmanager
    async def asyncconnected(self) -> "AsyncRedis": ...

    async def _recreated_pool(self) -> None: ...

    async def close(self) -> None: ...

    async def is_connected(self) -> bool: ...


class CacherAdapter(CacherBaseMixin, Protocol):
    _pool: ClassVar[
        Union["connection.ConnectionPool", "asyncConnection.ConnectionPool"]
    ]
    _pool_lock: ClassVar["threading.Lock"]

    def _init_pool(self) -> None: ...

    def __get_client(self) -> "Redis": ...

    def related(self) -> bool: ...

    @contextmanager
    def connected(self) -> "Redis": ...

    def _recreated_pool(self) -> None: ...

    def close(self) -> None: ...

    @property
    def is_connected(self) -> bool: ...


#
# class CacherAdapter(Protocol):
#     _pool: ClassVar[Optional[Any]] = None
#     _pool_lock: ClassVar[Optional["threading.Lock"]] = None
#
#     def _init_pool(self) -> None: ...
#
#     def __get_client(self) -> Optional["Redis"]: ...
#
#     def related(self) -> bool: ...
#
#     @contextmanager
#     def connected(self) -> "AbstractContextManager[Any]": ...
#
#     def _recreated_pool(self) -> None: ...
#
#     def close(self) -> None: ...
#
#     @property
#     def is_connected(self) -> bool: ...
#


class CacheManager(Protocol):

    async def asave(
        self, key: str, default: Optional[dict | list | tuple] = None, ttl: int = 300
    ) -> bool: ...

    def save(
        self, key: str, default: Optional[dict | list | tuple] = None, ttl: int = 300
    ) -> bool: ...

    async def aget(
        self,
        queue_collection: Optional["queue.Queue"] = None,
        collection: Optional[list | tuple] = None,
        key_pattern: Optional[str] = None,
        key: Optional[str] = None,
        ex: Optional[int] = None,
        px: Optional[int] = None,
        exat: Optional[int] = None,
        persist=None,
    ) -> Union[bool, "UsersPydantic"]: ...

    def get_sync(
        self,
        queue_collection: Optional["queue.Queue"] = None,
        collection: Optional[list | tuple] = None,
        key_pattern: Optional[str] = None,
        key: Optional[str] = None,
        ex: Optional[int] = None,
        px: Optional[int] = None,
        exat: Optional[int] = None,
        persist=None,
    ) -> Union[bool, "UsersPydantic"]: ...
