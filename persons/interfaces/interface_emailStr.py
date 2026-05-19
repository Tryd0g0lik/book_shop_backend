# persons/interfaces/interface_emailStr.py:2

from pydantic import EmailStr


class EmailString(EmailStr):

    @classmethod
    def __get_validators__(cls):

        yield from EmailStr.__get_validators__()

    def replace(self, old: str, new: str, count: int = -1) -> "EmailString":
        result = str(self).replace(old, new, count)
        return EmailString(result)
