# persons/exceptions/error_forms.py:2
from typing import Optional

from project import AbstractError


class ErrorCodeVerificationForm(AbstractError):
    def __init__(
        self, log_message: Optional[str] = "We do not have the valid form data!"
    ):
        super().__init__(log_message)
