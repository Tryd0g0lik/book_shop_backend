"""
persons/interfaces/interface_persons.py:1
This a content will use for how auxiliary classes for data typing.
"""

from datetime import datetime
from typing import Optional, TypedDict

from pydantic import BaseModel, ConfigDict

from persons.interfaces.interface_emailStr import EmailString


#
class UsersDict(TypedDict):
    id: Optional[str]
    is_superuser: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: str


class UsersPydanticDict(TypedDict):
    id: int
    last_login: Optional[datetime]
    is_superuser: bool
    username: str
    first_name: str
    last_name: str
    email: str
    is_staff: bool
    is_active: bool
    date_joined: datetime
    category: str
    password: str
    is_sent: bool
    is_verified: bool
    verification_code: Optional[str]
    balance: float
    created_at: datetime
    updated_at: datetime


class UsersPydantic(BaseModel):
    id: int
    last_login: Optional[datetime]
    is_superuser: bool
    username: str
    first_name: str
    last_name: str
    email: str
    is_staff: bool
    is_active: bool
    date_joined: datetime
    category: str
    password: str
    is_sent: bool
    is_verified: bool
    verification_code: Optional[str]
    balance: float
    created_at: datetime
    updated_at: datetime

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
