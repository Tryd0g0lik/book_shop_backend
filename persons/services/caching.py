"""
persons/adapters/caching.py:2
"""

import asyncio
import json
import logging
import queue
import re
from typing import Optional

from redis import ConnectionError

from persons.adapters import AsyncCacherAdapter, CacherAdapter

log = logging.getLogger(__name__)


class CacheManager:
    cacher = CacherAdapter(db=1)
    asynccacher = AsyncCacherAdapter(db=1)

    def __init__(
        self,
    ):
        self.log_t = "[CacheManager]:"

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
        log.info(
            """\n
# ============================================
# CACHE SERVER
# ============================================
# Checking of connection
            """
        )
        await self.asynccacher.related()
        is_connected = await self.asynccacher.is_connected()
        if is_connected is None or not is_connected:
            await self.asynccacher.related()
        log.info(
            """\n
# Here we make caching of data.
# ============================================
# SAVING DATA ON THE CACHE SERVER
# ============================================
            """
        )
        try:
            log.info(self.log_t[:-1] + "[asave]:" + " Before open the connection.")
            async with self.asynccacher.asyncconnected() as conn:
                log.info(self.log_t[:-1] + "[asave]:" + " Before caching the new data")
                existing = await conn.getex(key, ttl)
                log.info(
                    """\n
# ============================================
# WE MAKE A
# ============================================
                """
                )
                if existing is not None and existing:
                    log.info(
                        self.log_t[:-1]
                        + "[asave]:"
                        + " Cache's key: %s exists. TTL extended." % (key,)
                    )
                else:
                    if default is not None:
                        await conn.setex(
                            key,
                            ttl,
                            json.dumps(default, ensure_ascii=False).encode("utf-8"),
                        )
                del existing
                log.info(
                    self.log_t[:-1] + "[asave]:" + " Data was cached successfully!"
                )
        except Exception as e:
            log_t = " ".join(
                [
                    self.log_t[:-1] + "[asave]:",
                    " ERROR TEXT => %s ",
                    e.args[0] if e.args else str(e),
                ]
            )
            log.error(log_t)
            raise ValueError(log_t)
        return True

    async def aget(
        self,
        queue_collection: Optional[queue.Queue] = None,
        collection: Optional[list | tuple] = None,
        key_pattern: Optional[str] = None,
        key: Optional[str] = None,
        ex: Optional[int] = None,
        px: Optional[int] = None,
        exat: Optional[int] = None,
        persist=None,
    ):
        """
        You choose where could will saving data. It is the queue or the simple list
        :param str key_pattern: This is the template of key. Default value is None. Example 'user:pending:*'
        :param str key: This is the one key.Key which get the data from the cache serve. Default value is None.
            Example: 'user:pending:< user email has hot containing '.' & '@' characters >'
        :param queue.Queue queue_collection: This is a queue for collecting data from the cache server. Default value is None.
        :param list|tuple collection: This is a list of tuple  for collecting  data from the cache server. Default value is None.
        :param int ex: (PX milliseconds ) This is a time of caching. That is the cache time of life. At getex
        :param int px: milliseconds  This is a time of caching. That is the cache time of life At getex
        :param exat: Timestamp=seconds. Set the specified Unix time in seconds, Default value is None
        :param persist: Remove the existing timeout on key, turning the key, Default value is None
        :return:
        """
        log.info(
            self.log_t[:-1]
            + "[aget]:"
            + """\n
# ============================================
# CACHE SERVER
# ============================================
# Checking of connection
            """
        )
        await self.asynccacher.related()
        is_connected = await self.asynccacher.is_connected()
        if is_connected is None or not is_connected:
            await self.asynccacher.related()
        print(self.log_t[:-1] + "[aget]:" + "DEBUG WAS CONNECTED: %s" % is_connected)
        log.info(self.log_t[:-1] + "[aget]:" + "DEBUG WAS CONNECTED: %s" % is_connected)
        log.info(
            self.log_t[:-1]
            + "[aget]:"
            + """\n
# Here we make caching of data.
# ============================================
# GET DATA FROM THE CACHE
# ============================================
"""
        )
        try:
            log.info(self.log_t[:-1] + "[aget]:" + " Before open the connection.")
            async with self.asynccacher.asyncconnected() as conn:
                log.info(
                    " ".join([self.log_t[:-1], "[aget]:", "# Get keys from the cache."])
                )
                try:
                    log.info(
                        self.log_t[:-1]
                        + "[aget]:"
                        + """\n
# Get the cache's data by the keys.
# ============================================
# THE PATTERN OF KEY OR SINGLE KEY + CHOSE QUEUE OR LIST OR TUPLE
# ============================================
"""
                    )
                    if queue_collection is not None and isinstance(
                        queue_collection, queue.Queue
                    ):
                        log.info(
                            self.log_t[:-1]
                            + "[aget]:"
                            + " Before WORKING WITH A QUEUE & KEY_PATTERN"
                        )
                        if (
                            key_pattern is not None
                            or isinstance(key_pattern, str)
                            and re.search(r"[\w:]{1,50}", key_pattern, flags=re.ASCII)
                        ):
                            keys = await conn.keys(key_pattern)
                            if keys:

                                try:
                                    [queue_collection.put_nowait(k) for k in list(keys)]
                                except queue.Full:
                                    log.error(
                                        self.log_t[:-1] + "[aget]:"
                                        "Us need to increase the size of queue! There was not enough queue size"
                                    )
                        elif (
                            key is not None
                            or isinstance(key, str)
                            and re.search(r"[\w:]{1,50}", key, flags=re.ASCII)
                        ):
                            log.info(
                                self.log_t[:-1]
                                + "[aget]:"
                                + " WORKING To the  QUEUE & KEY & GETEX"
                            )

                            if (
                                ex is not None
                                and isinstance(ex, int)
                                or px is not None
                                and isinstance(ex, int)
                                or exat is not None
                                and isinstance(ex, int)
                                or persist is not None
                                and isinstance(ex, int)
                            ):
                                log.info(
                                    self.log_t[:-1]
                                    + "[aget]:"
                                    + " GET THE CACHE & PROLONGING THE TIME OF LIVE or persist"
                                )
                                value = await conn.getex(
                                    key, ex=ex, px=px, exat=exat, persist=persist
                                )
                                if value:
                                    collection.append(value)
                                    log.info(
                                        self.log_t[:-1]
                                        + "[aget]:"
                                        + " \nCOLLECTION Size: "
                                        + str(len(collection))
                                        + " \nCOLLECTION Content: "
                                        + str(collection)
                                    )
                            else:
                                log.info(
                                    self.log_t[:-1]
                                    + "[aget]:"
                                    + " SIMPLE GET THE CACHE PER A SINGLE KEY"
                                )

                                value = await conn.get(key)
                                if value:
                                    queue_collection.put_nowait(value)

                                    log.info(
                                        self.log_t[:-1]
                                        + "[aget]:"
                                        + " \nQUEUE_COLLECITON Size: "
                                        + str(queue_collection.qsize())
                                    )
                        else:
                            log_t = (
                                self.log_t[:-1]
                                + "[aget]:"
                                + " Data has not valid format! Check 'queue_collection key_pattern key' on the entrypoint."
                            )
                            log.error(log_t)
                            return False

                    elif (
                        collection is not None
                        and type(collection) is list
                        or type(collection) is tuple
                    ):
                        log.info(
                            self.log_t[:-1]
                            + "[aget]:"
                            + " Before WORKING WITH A COLLECTION & KEY_PATTERN"
                        )
                        log.info(
                            self.log_t[:-1]
                            + "[aget]:"
                            + "# WORKING WITH A LIST OR TUPLE"
                        )
                        if (
                            key_pattern is None
                            or isinstance(key_pattern, str)
                            and re.search(r"[\w:]{1,50}", key_pattern, flags=re.ASCII)
                        ):
                            keys = await conn.keys(key_pattern)
                            if keys:
                                collection.extend(list(keys))
                            # collection.extend(keys)
                            log.info(
                                self.log_t[:-1]
                                + "[aget]:"
                                + " \nKEYS Size: "
                                + str(len(collection))
                                + " \nKEYS Content: "
                                + str(collection)
                            )
                        elif (
                            key is None
                            or isinstance(key, str)
                            and re.search(r"[\w:]{1,50}", key, flags=re.ASCII)
                        ):
                            log.info(
                                self.log_t[:-1]
                                + "[aget]:"
                                + " Before WORKING WITH A COLLECTION & KEY & GETEX"
                            )
                            if (
                                ex is not None
                                and isinstance(ex, int)
                                or px is not None
                                and isinstance(ex, int)
                                or exat is not None
                                and isinstance(ex, int)
                                or persist is not None
                                and isinstance(ex, int)
                            ):
                                log.info(
                                    self.log_t[:-1]
                                    + "[aget]:"
                                    + " GET THE CACHE & PROLONGING THE TIME OF LIVE or persist"
                                )
                                value = await conn.getex(
                                    key, ex=ex, px=px, exat=exat, persist=persist
                                )
                                if value:
                                    collection.append(value)
                                    log.info(
                                        self.log_t[:-1]
                                        + "[aget]:"
                                        + " \nCOLLECTION Size: "
                                        + str(len(collection))
                                        + " \nCOLLECTION Content: "
                                        + str(collection)
                                    )
                            else:
                                log.info(
                                    self.log_t[:-1]
                                    + "[aget]:"
                                    + " SIMPLE GET THE CACHE PER A SINGLE KEY"
                                )
                                value = await conn.get(key)
                                if value:
                                    collection.append(value)
                                    log.info(
                                        self.log_t[:-1]
                                        + "[aget]:"
                                        + " \nCOLLECTION Size: "
                                        + str(len(collection))
                                        + " \nCOLLECTION Content: "
                                        + str(collection)
                                    )

                        else:
                            log_t = (
                                self.log_t[:-1]
                                + "[aget]:"
                                + " Data has not valid format! Check 'collection key_pattern key' on the entrypoint."
                            )
                            log.error(log_t)
                            return False
                    else:
                        log.info(
                            self.log_t[:-1]
                            + "[aget]:"
                            + " Data has not valid format! Check data on the entrypoint."
                        )
                        return False
                    log.info(
                        self.log_t[:-1] + "[aget]:" + " Data was cached successfully!"
                    )
                except Exception as e:
                    log.error(
                        self.log_t[:-1] + "[aget]:" + " ERROR TEXT => %s" % str(e)
                    )
                    return False
                log.info(
                    self.log_t[:-1]
                    + "[aget]:"
                    + " all successfully was saved in the queue."
                )
                if (
                    queue_collection is not None
                    and type(queue_collection) == asyncio.Queue
                ):
                    qsize = queue_collection.qsize()
                    log.info(self.log_t[:-1] + "[aget]:" + " Queue size: " + str(qsize))

                elif collection is not None and type(collection) == list | tuple:
                    size = len(collection)
                    log.info(
                        self.log_t[:-1] + "[aget]:" + " Storage size: " + str(size)
                    )
        except Exception as e:
            log_t = " ".join(
                [
                    self.log_t[:-1] + "[aget]:",
                    " ERROR TEXT => ",
                    e.args[0] if e.args else str(e),
                ]
            )
            log.error(log_t)
            raise ValueError(log_t)
        return True
