from typing import Optional

from project import AbstractError


class ProfileValueError(AbstractError):
    def __init__(
        self,
        log_message: Optional[
            str
        ] = "Check a role of user - Count specified roles must be one!",
    ):
        super().__init__(log_message)


class ProfileNotFound(AbstractError):
    def __init__(self, log_message: Optional[str] = "Role of user not defined!"):
        super().__init__(log_message)
