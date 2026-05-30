# persons/interfaces/interface_cache_adapter.py:3

from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Protocol, Union

if TYPE_CHECKING:
    import queue
    import threading
    from contextlib import AbstractContextManager

    from redis import Redis

    from persons.interfaces import UsersPydantic


class CacherBaseMixin(Protocol):

    @property
    def redis_password(self) -> str: ...

    @property
    def redis_master_name(self) -> str: ...

    @property
    def redis_database(self) -> int: ...


class CacherAdapter(Protocol):
    _pool: ClassVar[Optional[Any]] = None
    _pool_lock: ClassVar[Optional["threading.Lock"]] = None

    def _init_pool(self) -> None: ...

    def __get_client(self) -> Optional["Redis"]: ...

    def related(self) -> bool: ...

    @contextmanager
    def connected(self) -> "AbstractContextManager[Any]": ...

    def _recreated_pool(self) -> None: ...

    def close(self) -> None: ...

    @property
    def is_connected(self) -> bool: ...


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

    def get(
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
