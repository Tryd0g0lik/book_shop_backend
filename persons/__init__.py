"""
persons/__init__.py:1
"""

import re
from enum import Enum


class EnumEmailLetter(Enum):
    CONFIRM_EMAIL_Letter_0 = "account/email/email_confirmation_subject.txt"
    CONFIRM_EMAIL_Letter_1 = "account/email/email_confirmation_message.txt"


class EnumTemplatesKeysCache(Enum):
    """
    The '< email >' at the end of line has it from the 'test_address@mail.ru' in the 'test_addressmailru' view.
    :param 'user:pending:< email >' First letter of email/ Here we tell to
        the user  EnumEmailLetter.CONFIRM_EMAIL_Letter_0. TIme live 5 minutes.
    :param 'user:pending:letter_1:< email >' Message contain a secret code. Code to the verification email.
        TIme live 2 minutes or 120 seconds.
    :param 'user:pending:login: < email >' This is the key under which we save a jwt-state. Time live is 24 hours
        or 1440 minutes, or 86400 seconds. It means the data (in bytes): "{'is_superuser': < bool >, 'email': < EMAIL >,
         'category': < user_CATEGORY >,}"

    """

    USER_PENDING_0 = "user:pending:%s"
    USER_PENDING_LETTER_1 = "user:pending:letter_1:%s"
    USER_PENDING_LOGIN_0 = "user:pending:login:%s"


class EnumTemplatesREGEX(Enum):
    """
    :param PERSON_KEYS_OF_CACHE_IN_REGEX: This is templates of regex.
            Default belong the three expressions. Example this one from other: "r'(?P<name_all>user:pending:*)'".

    """

    PERSON_KEYS_OF_CACHE_IN_REGEX = re.compile(
        r"""^(
            (?P<name_expanded>user:pending:(login|letter_1):[a-zA-Z0-9_]{1,24}[a-zA-Z0-9])|
            (?P<name>user:pending:[a-zA-Z0-9_]{1,24}[a-zA-Z0-9])|
            (?P<name_all>user:pending:\*)
            )$""",
        re.VERBOSE | re.I,
    )
