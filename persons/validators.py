import logging

from django.core.validators import EmailValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from persons.models import Users

log = logging.getLogger(__name__)


@deconstructible
class EmailValidatorPerson(EmailValidator):
    def __call__(self, value):
        from django.core.exceptions import ValidationError

        # The maximum length of an email is 50 characters & min is 5
        # section 3.
        log.info(f"DEBUG VALIDATE EMAIL {value}: 1")
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
        log.info(f"DEBUG VALIDATE EMAIL {value}: 2")
        # if not self.validate_dublicate(value):
        #     log.info(f"DEBUG VALIDATE EMAIL {value}: 5")
        #     raise ValidationError(_("This email already exists."), code=self.code, params={"value": value})

    def validate_dublicate(self, email: str):

        log.info(f"DEBUG VALIDATE EMAIL {email}: 2")
        if Users.objects.filter(email=email).exists():
            log.info(f"DEBUG VALIDATE EMAIL {email}: 3")
            # raise forms.ValidationError(_("A user with this email already exists."))
            return False
        log.info(f"DEBUG VALIDATE EMAIL {email}: 4")

        return True


#
# @deconstructible
# class UsernameValidatorPerson:
#     def __call__(self, value: str):
#         from django.core.exceptions import ValidationError
#         if not  self.validate_dublicate(value):
#             raise ValidationError("Username already exists", code="invalid", params={"value": value})
#
#     def validate_dublicate(self, username: str = None):
#
#         if username is not None and  Users.objects.filter(username=username).exists():
#             return False
#
#         return True
