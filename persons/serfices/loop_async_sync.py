"""
persons/serfices/loop_async_sync.py:1
"""

import asyncio
import logging
from collections.abc import Coroutine
from datetime import datetime
from typing import Callable, TypeVar

log = logging.getLogger(__name__)

T = TypeVar("T")


class CostumizationSyncAsyncLoop:
    result = {
        "is_async": False,
    }

    def __init__(self, *args, **kwargs):
        self.__callback = None
        self.log_t = "[%s]:" % CostumizationSyncAsyncLoop.__class__.__name__
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
        if asyncio.iscoroutine(fun):
            self.result["is_async"] = True
        # Saving the 'fun' attribute
        self.__callback = fun

    @property
    def is_async(self):
        return self.result["is_async"]

    @is_async.setter
    def is_async(self, val: bool) -> None:
        self.result["is_async"] = val
        # if isinstance(self.get_new_function, Coroutine):

    def get_new_loop(self) -> Callable[[], T]:
        is_async = self.result["is_async"]
        if self.get_new_function is None:
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
                callback = self.get_new_function

                # --- Async Callback
                def async_wrapper():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        return loop.run_until_complete(callback(*args, **kwargs))
                    finally:
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
            callback = self.get_new_function

            # --- Sync Callback
            def sync_wrapper():
                return callback(*args, **kwargs)

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
