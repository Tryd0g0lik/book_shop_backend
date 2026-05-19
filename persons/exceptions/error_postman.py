"""
persons/exceptions/error_postman.py:1
"""

from typing import Optional


class PostmanRequiredModelError(Exception):
    """The requested model field does not exist"""

    def __init__(self, log_message="Required name of database does not exists."):
        self._log_message = log_message
        message: Optional[str] = "[%s]" % self.__class__.__name__
        if self._log_message is not None and self._log_message != "":
            message += self._log_message
        super().__init__(message)
