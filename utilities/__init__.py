from enum import Enum


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

    USER_PENDING_ZERO = "user:pending:zero:%s"
    USER_PENDING_LETTER = "user:pending:letter:%s"
    USER_PENDING_LOGIN = "user:pending:login"
