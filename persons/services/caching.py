"""
persons/services/caching.py:4
"""

import asyncio
import json
import logging
import queue
import re
import threading
from typing import Coroutine, Optional

from persons.adapters import AsyncCacherAdapter, CacherAdapter
from persons.interfaces import AsyncCacherAdapter as AsyncCacherAdapterInitialize
from persons.interfaces import CacherAdapter as CacherAdapterInitialize
from project.settings_conf.settings_env import REDIS_DB

log = logging.getLogger(__name__)

log.info(f"DEBUG REDIS_DB: {REDIS_DB}")


class CacheManager:

    def __init__(
        self,
    ):
        self.log_t = f"{__name__.split("/")[-1]}" + "[CacheManager]:"
        self.asynccacher: AsyncCacherAdapterInitialize = AsyncCacherAdapter(db=REDIS_DB)

    async def asave(
        self, key: str, default: Optional[dict | list | tuple] = None, ttl: int = 300
    ) -> bool:
        """
        :return: bool
        :param key: This is a key of caching. That we use to get the data.
        :param default:
        :param ttl: Seconds. This is a time of caching. That is the cache time of life.
        :return: bool
        """
        is_connected = await self.asynccacher.is_connected()
        if is_connected is not None or not is_connected:
            await self.asynccacher.related()
        log.info(
            """\n
# ============================================
# CACHE SERVER ASAVE
# ============================================
# Checking of connection
            """
        )
        #
        # is_connected = await self.asynccacher.is_connected()
        # if is_connected is None or not is_connected:
        #     await self.asynccacher.related()
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
                if existing is not None:
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
                # The clean storage
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

    def save(
        self, key: str, default: Optional[dict | list | tuple] = None, ttl: int = 300
    ) -> bool:
        """
        :return: bool
        :param key: This is a key of caching. That we use to get the data.
        :param default:
        :param ttl:  This is a time of caching. That is the cache time of life.
        :return: bool
        """
        from persons.services import CustomizationSyncAsyncLoop

        log.info(
            self.log_t[:-1]
            + "[aget]:"
            + """\n
        # ============================================
        # CACHE SERVER SAVE
        # ============================================
        # Checking of connection
                    """
        )
        try:
            loop_async_sync = CustomizationSyncAsyncLoop(
                *[], **{"key": key, "default": default, "ttl": ttl}
            )
            loop_async_sync.get_new_function = self.asave
            loop_async_sync.is_async = True
            log.info("DEBUG VALUE BOOL  before coroutine")
            if loop_async_sync.is_async:
                coroutine_in_new_loop = loop_async_sync.get_new_loop()
                value_bool = coroutine_in_new_loop()
                log.info("DEBUG VALUE BOOL  from coroutine: %s " % value_bool)

            log_t = " ".join(
                [
                    self.log_t[:-1] + "[save]:",
                    "Check a new loop. THe ASAVE method don't run in the sync loop.",
                ]
            )
            log.error(log_t)
            raise ValueError(log_t)
        except Exception as e:
            log.error(e.args if e.args else str(e))
            raise e

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
    ) -> Optional[bool]:
        """
        You choose where could will saving the get's data. In the queue or the simple list.
        :param str key_pattern: This is the template of key. Default value is None. Example 'user:pending:*'
        :param str key: This is the one key.Key which get the data from the cache serve. Default value is None.
            Example: 'user:pending:< user email has hot containing '.' & '@' characters >'
        :param queue.Queue queue_collection: This is a queue for collecting data from the cache server. Default value is None.
        :param list|tuple collection: This is a list of tuple  for collecting  data from the cache server. Default value is None.
        :param int ex: (PX milliseconds ) This is a time of caching. That is the cache time of life. At getex
        :param int px: milliseconds  This is a time of caching. That is the cache time of life At getex
        :param exat: Timestamp=seconds. Set the specified Unix time in seconds, Default value is None
        :param persist: Remove the existing timeout on key, turning the key, Default value is None
        :return: Optional[bool] If return the True mean oll successfully or mistake.
        """
        is_connected = await self.asynccacher.is_connected()
        if is_connected is not None or not is_connected:
            await self.asynccacher.related()
        log.info(
            self.log_t[:-1]
            + "[aget]:"
            + """
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
                            and isinstance(key_pattern, str)
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
                            else:
                                return None
                        elif (
                            key is not None
                            and isinstance(key, str)
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
                                and isinstance(px, int)
                                or exat is not None
                                and isinstance(exat, int)
                                or persist is not None
                                and isinstance(persist, int)
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
                                    queue_collection.put_nowait(value)
                                    log.info(
                                        self.log_t[:-1]
                                        + "[aget]:"
                                        + " \nCOLLECTION Size: "
                                        + str(queue_collection.qsize())
                                        + " \nCOLLECTION Content: "
                                        + str(queue_collection)
                                    )
                                else:
                                    return None

                            else:
                                log.info(
                                    self.log_t[:-1]
                                    + "[aget]:"
                                    + f" SIMPLE GET THE CACHE PER A SINGLE KEY: {key}"
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
                                    return None
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
                            + "DEBUG: %s & Key: %s" % (str(key_pattern), str(key))
                        )
                        if (
                            key_pattern is not None
                            or isinstance(key_pattern, str)
                            and re.search(r"[\w:]{1,50}", key_pattern, flags=re.ASCII)
                        ):
                            keys = await conn.keys(key_pattern)
                            log.info(
                                self.log_t[:-1] + "[aget]:" + " \nKEYS: " + str(keys)
                            )
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
                            key is not None
                            and isinstance(key, str)
                            and re.search(r"[\w:]{1,50}", key, flags=re.ASCII)
                        ):
                            log.info(
                                self.log_t[:-1]
                                + "[aget]:"
                                + " Before WORKING WITH A COLLECTION & KEY & GETEX"
                            )
                            if (
                                (ex is not None and isinstance(ex, int))
                                or (px is not None and isinstance(px, int))
                                or (exat is not None and isinstance(exat, int))
                                or (persist is not None and isinstance(persist, int))
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
                                    return None
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
                                    return None

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

    #
    def get_sync(
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
        # CACHE SERVER GET
        # ============================================
        # Checking of connection
    """
        )
        try:
            from redis import ConnectionError

            from persons.services import CustomizationSyncAsyncLoop

            qwargs = {
                "queue_collection": queue_collection,
                "collection": collection,
                "key_pattern": key_pattern,
                "key": key,
                "ex": ex,
                "px": px,
                "exat": exat,
                "persist": persist,
            }
            # return self.aget(**qwargs)
            loop = None
            try:
                # Получаем текущий или создаём новый event loop
                loop = asyncio.get_running_loop()
            except RuntimeError:
                # Нет запущенного цикла — создаём новый
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                # Выполняем корутину и получаем результат
            get_data = loop.run_until_complete(self.aget(**qwargs))
            return get_data
        except Exception as e:
            log.error(e.args if e.args else str(e))
            raise e
