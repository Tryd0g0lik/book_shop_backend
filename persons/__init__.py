"""
persons/__init__.py:1
"""

import re
from enum import Enum

from project.settings_conf.settings_env import APP_NAME

CATEGORY_STATUS = [
    ("BASE", "Base"),
    ("ADMIN", "Admin"),
    ("MANAGER", "Manager"),
    ("CLIENT", "Client"),
    ("MODERATORS", "Moderators"),
]
PATH_NAMES: list[str] = [
    "/person/register/account/",
    "/person/register/admin/",
    "/person/register/moderators/",
    "/person/register/manager/",
    "/person/register/client/",
]


class EnumEmailLetter(Enum):
    CONFIRM_EMAIL_Letter_0 = "account/email/email_confirmation_signup_message.txt"
    CONFIRM_EMAIL_Letter_1 = "account/email/email_confirmation_message.txt"
    CONFIRM_EMAIL_Letter_2 = "account/email/email_confirm_message.txt"


class EnumTemplatesREGEX(Enum):
    """
    :param PERSON_KEYS_OF_CACHE_IN_REGEX: This is templates of regex.
            Default belong the three expressions. Example this one from other: "r'(?P<name_all>user:pending:*)'".

    """

    PERSON_KEYS_OF_CACHE_IN_REGEX = re.compile(
        r"""^(
            (?P<name_expanded>user:pending:(login|letter_1):[a-zA-Z0-9_]{1,24}[a-zA-Z0-9])|
            (?P<name>user:pending:(zero|letter):[a-zA-Z0-9_]{1,24}[a-zA-Z0-9])
            )$""",
        re.VERBOSE | re.I,
    )


class EnuSubjectOfLetter(Enum):
    """
    This is Subject/Theme for Letters.
    < Name of task >_< Index of key>. Example: @shared_task['name'] = 'sub_task_get_send_letter' & 0 that is the index.
    """

    SUB_TASK_GET_SEND_LETTER_0 = APP_NAME + " Thanks for your account"
