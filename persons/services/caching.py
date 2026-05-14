"""
persons/adapters/caching.py:2
"""

import asyncio
import json
import logging
from typing import Optional

from redis import ConnectionError

from persons.adapters import AsyncCacherAdapter, CacherAdapter

log = logging.getLogger(__name__)


class CacheManager:
    cacher = CacherAdapter(db=1)
    asynccacher = AsyncCacherAdapter(db=1)
    _async_lock = asyncio.Lock()

    def __init__(
        self,
    ):
        self.log_t = "[%s]:" % CacheManager.__class__.__name__

    async def asave(
        self, key: str, default: Optional[dict | list | tuple] = None, ttl: int = 300
    ) -> bool:
        """
        :return: bool
        :param key: This is a key of caching. That we use to get the data.
        :param default:
        :param ttl:  This is a time of caching. That is the cache time of life.
        :return: bool
        """
        print("DEBUG Key: %s" % key)
        print("DEBUG default: %s" % str(default))
        print("DEBUG ttl: %s" % str(ttl))
        # ============================================
        # CACHE SERVER
        # ============================================
        # Checking of connection
        await self.asynccacher.related()
        is_connected = await self.asynccacher.is_connected()
        print("DEBUG is_connected: %s" % str(is_connected))
        if is_connected is None or not is_connected:
            is_connected = await self.asynccacher.related()
        print("DEBUG WAS CONNECTED: %s" % is_connected)
        # Here we make caching of data.
        # ============================================
        # SAVING DATA BEFORE REGISTRATION
        # ============================================
        try:
            # asyncconnected = self.asynccacher.asyncconnected
            look = self._async_lock
            print("DEBUG async lock: %s" % str(look))
            async with look:
                async with self.asynccacher.asyncconnected() as conn:
                    log.info(self.log_t + " Before caching the new data")
                    print(f"DEBUG {self.log_t} Before caching the new data")
                    existing = await conn.getex(key, ttl)
                    if existing is not None and existing:
                        log.info(
                            self.log_t
                            + " Cache's key: %s exists. TTL extended." % (key,)
                        )
                        print(
                            f"DEBUG {self.log_t} Cache's key: %s exists. TTL extended."
                        )
                    else:
                        if default is not None:
                            await conn.setex(
                                key,
                                ttl,
                                json.dumps(default, ensure_ascii=False).encode("utf-8"),
                            )
                            print(f"DEBUG {self.log_t} Cache was SETEX.")
                    del existing
                    log.info(self.log_t + " Data was cached successfully!")
                    print(f"DEBUG {self.log_t} Data was cached successfully!")
        except Exception as e:
            log_t = " ".join(
                [self.log_t, " Cache Error: ", e.args[0] if e.args else str(e)]
            )
            print("DEBUG ERROR in saving into Redis DB: %s " % log_t)
            log.error(log_t)
            raise ValueError(log_t)
        return True
