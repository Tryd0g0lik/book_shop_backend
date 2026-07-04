import logging

from django.core.validators import EmailValidator
from django.utils.deconstruct import deconstructible

from persons.models import Users

log = logging.getLogger(__name__)


@deconstructible
class EmailValidatorPerson(EmailValidator):
    def __call__(self, value):
        from django.core.exceptions import ValidationError

        # The maximum length of an email is 50 characters & min is 5
        # section 3.
        if (
            not value or "@" not in value or len(value) > 50 or len(value) < 5
        ):  # It is updated
            raise ValidationError(self.message, code=self.code, params={"value": value})

        user_part, domain_part = value.rsplit("@", 1)

        if not self.user_regex.match(user_part):
            raise ValidationError(self.message, code=self.code, params={"value": value})

        if domain_part not in self.domain_allowlist and not self.validate_domain_part(
            domain_part
        ):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def validate_dublicate(self, email: str):
        if Users.objects.filter(email=email).exists():
            return False

        return True
