"""
persons/adapters/person_base.py:1
"""

from typing import Optional, Union

from persons.interfaces import UsersPydantic, UsersPydanticDict

# from persons.exceptions import PersonErrorImproperlyConfigured
from ..exceptions.error_postman import PostmanRequiredModelError

# from pydantic import EmailStr


# from wagtail.compat import AUTH_USER_MODEL


class PersonBasisMixin:
    def __init__(
        self,
        log_t: str,
        person_index: Optional[int] = None,
        person_email: Optional[str] = None,
    ):
        self.__person_index: Optional[int] = person_index
        self.__person_email: Optional[str] = person_email
        self.__person_model: Optional[UsersPydantic] = None
        self.__key_of_cache: Optional[str] = None
        self.log_t: str = log_t[:-1] + f"[{self.__class__.__name__}]:"

    @property
    def get_person_model(self) -> Optional[UsersPydantic] | None:
        return self.__person_model

    @get_person_model.setter
    def get_person_model(self, value: Optional[UsersPydanticDict] = None) -> None:
        # self._is_person(value)
        self.__person_model = value

    @property
    def get_email(self) -> str:
        return self.__person_email

    @get_email.setter
    def get_email(
        self, email: Optional[str] = None, value: Optional[UsersPydantic] = None
    ) -> None:
        if email is None and value is None:
            raise PostmanRequiredModelError(
                " The value is not None - Check. The required variable "
            )

        if value is not None:
            # self._is_person(value)
            self.__person_email = value.__getattr__("email")
        else:
            self.__person_email = email

    @property
    def get_index(self) -> int:
        return self.__person_index

    @get_index.setter
    def get_index(
        self, index: Optional[int] = None, value: Optional[UsersPydantic] = None
    ) -> None:
        if index is None and value is None:
            raise PostmanRequiredModelError(
                " The value is not None - Check. The required variable"
            )

        if value is not None:
            # self._is_person(value)
            self.__person_index = value.__getattr__("id")
        else:
            self.__person_index = index

    @staticmethod
    def _is_person(value=None) -> bool:
        """
        :param value: The value this is variable must be belonging to the Users model.
        :return bool: The 'True' it's if all Ok or return mistake 'PostmanRequiredModelError'
        """
        from persons.exceptions.error_postman import PostmanRequiredModelError

        # The value is not None - Check
        if value is None:
            raise PostmanRequiredModelError(
                " The value is not None - Check. The required variable \
is invalid."
            )
        # The value belonging to the Users's model or not (is not object person) - Check
        if not isinstance(value, Union[UsersPydantic]):
            raise PostmanRequiredModelError(
                " The value belonging to the Users's model or not (is not \
object person) - Check. Do not belonging to the Users's model."
            )
        return True

    @property
    def get_key_cache(self) -> str:
        """
        Key name from the cache server. Default value is the None.
        :return str. returning the one key from the these:
        - 'user:pending:< email >';
        - 'user:pending:letter:< email >';
        - 'user:pending:login: < email >';
        - 'user:pending:*'.
        """
        return self.__key_of_cache

    @get_key_cache.setter
    def get_key_cache(self, value: str) -> None:
        """
        The all values on the entrance could hase the next template:
        - 'user:pending:< email >';
        - 'user:pending:letter:< email >';
        - 'user:pending:login';
        - 'user:pending:*'.
        If it is an email's value that mean the '< email >' at end of line. It ('test_address@mail.ru') is from
            our line - the 'test_addressmailru'.
            Or. The value has '*' (means the all email). That could be the 'test_address@mail.ru' or
            'testemail@rambler.ru' and more.
        :param str value:

        :return: Void or mistake 'PostmanRequiredModelError'
        """
        try:
            # Check a key of CACHE.
            self._is_key_of_cache(value)
            # Get of result
            self.__key_of_cache = value.strip()
        except Exception as e:
            raise e

    def _is_key_of_cache(self, value: str) -> bool:
        """
        :param value:
        :return: True or mistake 'PostmanRequiredModelError'
        """
        from .. import EnumTemplatesKeysCache

        # The value is not None - Check
        if value is None:
            raise PostmanRequiredModelError(
                self.log_t
                + ": The value is not None - Check. The required variable \
                    is invalid."
            )

        # Regex expression - Check
        result_from_the_regex_expression = self.KEY_OF_CACHE_REGEX.search(value)
        if (
            value is not UsersPydantic.email
            and result_from_the_regex_expression is None
        ):
            raise PostmanRequiredModelError(
                self.log_t
                + ": Regex expression - Check. The required variable is \
                    invalid. The value is not email."
            )

        keys = [k.value for k in EnumTemplatesKeysCache]
        val = "".join(list(value.split(":"))[:-1])
        # The template of value it is one from list - Check
        if val not in keys:
            raise PostmanRequiredModelError(
                self.log_t
                + ": The template is one from the all list - Check. \
                    The required name of key is not found at the common list of template of keys ."
            )
        return True
