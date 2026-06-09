"""
persons/services/loop_async_sync.py:1
"""

import asyncio
import logging
from collections.abc import Coroutine
from datetime import datetime
from typing import Callable, TypeVar

log = logging.getLogger(__name__)

T = TypeVar("T")


class CustomizationSyncAsyncLoop:
    result = {
        "is_async": False,
    }

    def __init__(self, *args: tuple | list, **kwargs: dict):
        self.__callback = None
        self.log_t = "[%s]:" % CustomizationSyncAsyncLoop.__class__.__name__
        self.log_datetime = datetime
        self.args = args
        self.kwargs = kwargs

    @property
    def get_new_function(self) -> Coroutine | Callable[[T], T]:
        return self.__callback

    @get_new_function.setter
    def get_new_function(self, fun) -> None:
        """
        TODO: На входе получаем функцию.
            Проверяем на асинхронность.
            На выходе ('get_new_loop()') возвращаем вункцию для запуска в 'threading.Thread(target=sync_fun, args, kwargs)'.)

        :param fun: This is the sync function or coroutine.
        Example:```
            def example_function(*args, **kwargs):
                pass
            async def async_example_function(*args, **kwargs):
                pass
            obj.get_new_function(example_function):
                self.is_async = example_function # True
                self.is_async = example_function() # False
                # or
                self.is_async = async_example_function # True
                self.is_async = async_example_function() # False
        ```
        """
        if not callable(fun):
            try:
                self.log_t += " ".join(
                    [
                        " ",
                        self.log_datetime.now().strftime("%Y-%m-%d %H:%M:%S.%m"),
                        " The 'fun' argument must be a sync function or coroutine.",
                    ]
                )
                log.error(self.log_t)
                raise TypeError(self.log_t)
            finally:
                self.log_t = self.log_t.split("]: ")[0] + "]:"
        # Check the 'fun' attribute is coroutine or not
        if asyncio.iscoroutine(fun) or asyncio.iscoroutinefunction(fun):
            self.result["is_async"] = True
        # Saving the 'fun' attribute
        self.__callback = fun

    @property
    def is_async(self):
        return self.result["is_async"]

    @is_async.setter
    def is_async(self, val: bool) -> None:
        self.result["is_async"] = val

    def get_new_loop(self) -> Callable[[], T]:
        is_async = self.result["is_async"]
        callback = self.get_new_function

        if callback is None:
            TEXT_ERROR = " ".join(
                [
                    self.log_t,
                    self.log_datetime.now().strftime("%Y-%m-%d %H:%M:%S.%m"),
                    " The 'get_new_function' not valis.",
                ]
            )
            raise ValueError(TEXT_ERROR)

        if is_async:

            try:
                args = self.args
                kwargs = self.kwargs

                # ============================================
                # ASYNC CALLBACK
                # ============================================
                def async_wrapper():
                    log.info("Start ASYNC writing to the cache server")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:

                        return loop.run_until_complete(callback(*args, **kwargs))
                    except Exception as e:
                        log.error(
                            "Writing ASYNC to the cache server failed! TEXT_ERROR: %s"
                            % e.args[0]
                            if e.args
                            else str(e)
                        )
                    finally:
                        log.info("Finish ASYNC writing to the cache server,")
                        loop.close()

                return async_wrapper
            except ConnectionError as e:
                TEXT_ERROR = " ".join(
                    [
                        self.log_t,
                        " ConnectionError: ",
                        self.log_datetime.now().strftime("%Y-%m-%d %H:%M:%S.%m"),
                        e.args[0] if e.args else str(e),
                    ]
                )
                raise ValueError(TEXT_ERROR)
            except Exception as e:
                TEXT_ERROR = " ".join(
                    [
                        self.log_t,
                        " Error: ",
                        self.log_datetime.now().strftime("%Y-%m-%d %H:%M:%S.%m"),
                        e.args[0] if e.args else str(e),
                    ]
                )
                raise ValueError(TEXT_ERROR)
            finally:
                pass
        try:
            args = self.args
            kwargs = self.kwargs

            # ============================================
            # SYNC CALLBACK
            # ============================================
            def sync_wrapper():
                try:
                    log.info("Start SYNC writing to the cache server")
                    return callback(*args, **kwargs)
                except Exception as e:
                    log.error(
                        "Writing SYNC to the cache server failed! TEXT_ERROR: %s"
                        % e.args[0]
                        if e.args
                        else str(e)
                    )
                finally:
                    log.info("Finish SYNC writing to the cache server,")

            return sync_wrapper
        except ConnectionError as e:
            TEXT_ERROR = " ".join(
                [
                    self.log_t,
                    " ConnectionError: ",
                    self.log_datetime.now().strftime("%Y-%m-%d %H:%M:%S.%m"),
                    e.args[0] if e.args else str(e),
                ]
            )
            raise ValueError(TEXT_ERROR)
        except Exception as e:
            TEXT_ERROR = " ".join(
                [
                    self.log_t,
                    " Error: ",
                    self.log_datetime.now().strftime("%Y-%m-%d %H:%M:%S.%m"),
                    e.args[0] if e.args else str(e),
                ]
            )
            raise ValueError(TEXT_ERROR)
        finally:
            pass
