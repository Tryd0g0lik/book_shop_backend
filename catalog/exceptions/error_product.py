# catalog/exceptions.py:
from typing import Optional

from project import AbstractError


class ProductValueError(AbstractError):
    def __init__(self, log_message="The value is not valid"):
        self._log_message = log_message
        message: Optional[str] = "[%s]" % self.__class__.__name__
        if self._log_message is not None and self._log_message != "":
            message += self._log_message
        super().__init__(message)
