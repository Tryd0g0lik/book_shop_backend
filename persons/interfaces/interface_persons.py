"""
persons/interfaces/interface_persons.py:1
This a content will use for how auxiliary classes for data typing.
"""

from datetime import datetime
from typing import Optional, Protocol, TypedDict, Union
from unicodedata import category

from django.utils import timezone

# from django.contrib.auth.models import Group
from pydantic import BaseModel, ConfigDict

from persons.interfaces.interface_emailStr import EmailString


class Users(Protocol):
    username_validator: str
    username: str
    first_name: str
    last_name: str
    email: EmailString
    password: str
    is_sent: bool
    is_staff: bool
    is_active: bool
    is_verified: bool
    verification_code: str
    balance: float
    date_joined = timezone
    created_at = timezone
    updated_at: timezone
    user_permission: list
    groups: list
    is_superuser: bool

    def __str__(self) -> str: ...

    def clean_verification_code(self) -> None: ...

    def clean(self) -> None: ...

    def get_full_name(self) -> str: ...

    def get_short_name(self) -> str: ...

    def email_user(self, subject, message, from_email=None, **kwargs) -> None: ...
    def save(self, **kwargs) -> None: ...

    def get_username(self) -> Optional[str]: ...

    def natural_key(self): ...

    @property
    def is_anonymous(self) -> bool: ...
    @property
    def is_authenticated(self) -> bool: ...

    def set_password(self, raw_password) -> None: ...

    def check_password(self, raw_password):
        def setter(raw_password): ...

    async def acheck_password(self, raw_password):
        async def setter(raw_password): ...

    def set_unusable_password(self) -> None: ...

    def has_usable_password(self) -> str: ...

    def get_session_auth_hash(self): ...

    def get_session_auth_fallback_hash(self) -> None: ...

    def _get_session_auth_hash(self, secret=None): ...

    @classmethod
    def get_email_field_name(cls) -> str: ...

    @classmethod
    def normalize_username(cls, username): ...


class UsersDict(TypedDict):
    id: Optional[str]
    is_superuser: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: str


class UsersPydanticDict(ConfigDict):
    id: Optional[int]
    last_login: Optional[Union[datetime, str]]
    is_superuser: Optional[bool]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    is_staff: Optional[bool]
    is_active: Optional[bool]
    date_joined: Optional[Union[datetime, str]]
    category: Optional[str]
    password: Optional[str]
    is_sent: Optional[bool]
    is_verified: Optional[bool]
    verification_code: Optional[str]
    balance: Optional[float]
    created_at: Optional[Union[datetime, str]]
    updated_at: Optional[Union[datetime, str]]


class UsersPydantic(BaseModel):
    id: Optional[int]
    last_login: Optional[datetime]
    is_superuser: Optional[bool]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    is_staff: Optional[bool]
    is_active: Optional[bool]
    date_joined: Optional[datetime]
    password: Optional[str]
    is_sent: Optional[bool]
    is_verified: Optional[bool]
    verification_code: Optional[str]
    balance: Optional[float]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def to_dict_without_secret_data(self) -> dict:
        """We are excepts the password/ verification_code field from dict"""

        data_dict: dict = self.model_dump(
            exclude={
                "password",
                "verification_code",
                "last_login",
                "updated_at",
                "created_at",
                "date_joined",
            }
        )
        category = self.get_category()

        data_dict.__setitem__("category", category if category is not None else None)

        if self.last_login is not None:
            data_dict.__setitem__(
                "last_login", self.last_login.strftime("%m-%d-%Y_%H:%M:%S")
            )
        if self.last_login is not None:
            data_dict.__setitem__(
                "last_login", self.last_login.strftime("%m-%d-%Y_%H:%M:%S")
            )
        if self.updated_at is not None:
            data_dict.__setitem__(
                "updated_at", self.updated_at.strftime("%m-%d-%Y_%H:%M:%S")
            )
        if self.created_at is not None:
            data_dict.__setitem__(
                "created_at", self.created_at.strftime("%m-%d-%Y_%H:%M:%S")
            )
        if self.date_joined is not None:
            data_dict.__setitem__(
                "date_joined", self.date_joined.strftime("%m-%d-%Y_%H:%M:%S")
            )
        return data_dict

    def to_public_dict(self) -> dict:
        """Field only for publication"""

        data_dict: dict = self.model_dump(
            include={
                "id",
                "username",
                "email",
                "first_name",
                "last_name",
                "balance",
                "category",
                "is_superuser",
                "is_staff",
                "is_active",
                "is_sent",
                "is_verified",
            }
        )
        category = self.get_category()

        data_dict.__setitem__("category", category if category is not None else None)

        if self.last_login is not None:
            data_dict.__setitem__(
                "last_login", self.last_login.strftime("%m-%d-%Y_%H:%M:%S")
            )
        return data_dict

    model_config = ConfigDict(from_attributes=True)

    def clean(self):
        """Clean the user's data."""
        pass

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self) -> str:
        """Return the short name for the user."""
        return self.first_name

    def send_email_user(
        self, subject: str, message: str, from_email: Optional[str] = None, **kwargs
    ) -> None:
        """Send an email to this user."""
        pass

    def get_category(self) -> Optional[str]:
        # from persons.models import Users
        from django.contrib.auth import get_user_model

        Users = get_user_model()
        if self.id:
            queryset = Users.objects.filter(id=self.id)
            user = queryset.first() if queryset.count() > 0 else None
            if user:
                group_names = user.groups.values_list("name", flat=True)
                group_names_str = ",".join(group_names)
                return group_names_str
        return None
