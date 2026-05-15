"""
persons/__init__.py:1
"""

from enum import Enum


class EnumEmailLetter(Enum):
    CONFIRM_EMAIL_Letter_0 = "account/email/email_confirmation_subject.txt"
    CONFIRM_EMAIL_Letter_1 = "account/email/email_confirmation_message.txt"


class EnumTemplatesKeysCache(Enum):
    """
    :param 'user:pending:< email >' First letter of email/ Here wa tell to the user  EnumEmailLetter.CONFIRM_EMAIL_Letter_0
    :param '"user:pending:letter_1:< email >' Message contain a secret code. Code to the verification email.
    """

    USER_PENDING_0 = "user:pending:%s"
    USER_PENDING_LETTER_1 = "user:pending:letter_1:%s"
