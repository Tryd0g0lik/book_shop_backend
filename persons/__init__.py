"""
persons/__init__.py:1
"""

import re
from enum import Enum

from typing_extensions import TypeAlias

from project.settings_conf.settings_env import APP_NAME

CATEGORY_STATUS = [
    ("BASE", "Base"),
    ("ADMIN", "Admin"),
    ("MANAGER", "Manager"),
    ("CLIENT", "Client"),
]


class EnumEmailLetter(Enum):
    CONFIRM_EMAIL_Letter_0 = "account/email/email_confirmation_subject.txt"
    CONFIRM_EMAIL_Letter_1 = "account/email/email_confirmation_message.txt"
    CONFIRM_EMAIL_Letter_2 = "account/email/email_confirm_message.txt"


class EnumTemplatesKeysCache(Enum):
    """
    The '< email >' at the end of line has it is from the 'test_address@mail.ru' in the 'test_addressmailru' view.
    :param 'user:pending:< email >' First letter of email/ Here we tell to
        the user  EnumEmailLetter.CONFIRM_EMAIL_Letter. TIme live 5 minutes.
        Template: 'user:pending:< email >': '{"username": < USERNAME >, "email": < EMAIL >}'
    :param 'user:pending:letter:< email >' Message contain a secret code. Code to the verification email.
        TIme live 2 minutes or 120 seconds.
         Example 'user:pending:letter:< email >':'{"username": < USERNAME >, "email": < EMAIL >, ....}'
    :param 'user:pending:login'  This person must be having a status 'is_active' and 'is_verified'!
        This is the key under which we are using how session's data. Time live is 24 hours
        or 1440 minutes, or 86400 seconds. It means the value of data (in bytes): bytes'"[{'is_superuser': < bool >,
        'email': < EMAIL >,'category': < user_CATEGORY >},]"'.
         Note: Here < EMAIL > it is required element. It is a key for lookup the element.
         Time live: 86400

    """

    USER_PENDING = "user:pending:%s"
    USER_PENDING_LETTER = "user:pending:letter:%s"
    USER_PENDING_LOGIN = "user:pending:login"


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


class EnuSubjectOfLetter(Enum):
    """
    This is Subject/Theme for Letters.
    < Name of task >_< Index of key>. Example: @shared_task['name'] = 'sub_task_get_send_letter' & 0 that is the index.
    """

    SUB_TASK_GET_SEND_LETTER_0 = APP_NAME + " Thanks for your account"
