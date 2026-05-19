"""
persons/interfaces/interface_persons.py:1
This a content will use for how auxiliary classes for data typing.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from persons.interfaces.interface_emailStr import EmailString


class UsersPydantic(BaseModel):
    id: int
    last_login: Optional[datetime]
    is_superuser: bool
    username: str
    first_name: str
    last_name: str
    email: EmailString
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

    class Config:
        from_attributes = True

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
