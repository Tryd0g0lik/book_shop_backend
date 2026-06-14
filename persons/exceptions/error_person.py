"""
persons/exceptions/error_person.py:4
Arial by error from the Person app.
"""

from typing import Optional

from persons.exceptions.error_basis import PersonError


class PersonErrorImproperlyConfigured(PersonError):
    def __init__(self, log_message: Optional[str] = "We do not have the valid data!"):
        super().__init__(log_message)


# Error of tasks
class PersonErrorTasks(PersonError):
    def __init__(self, log_message: Optional[str] = "We do not have the valid data!"):
        super().__init__(log_message)


class PersonLogingError(PersonError):
    def __init__(self, log_message: Optional[str] = "We do not have the valid data!"):
        super().__init__(log_message)
