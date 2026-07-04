"""
persons/forms/users_registration_form.py:1
"""

import json
import logging
import re

from allauth.account.forms import SignupForm, UserTokenForm
from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
)
from django.utils.translation import gettext_lazy as _

from persons import CATEGORY_STATUS
from persons.models import Users
from persons.validators import EmailValidatorPerson

# from persons.services import CacheManager
from project.settings_conf.settings_env import (
    APP_MAX_PASSWORD_LENGTH,
    APP_MINIMUM_PASSWORD_LENGTH,
)

log = logging.getLogger(__name__)


class UsersRegistrationForm(SignupForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     # We don't know a view of the password1/password2 filed. They could be the 'forms.CharField' or
    #     # 'forms.PasswordInput' or anything else.
    #     if "password1" in self.fields:
    #         field_password1 = self.fields["password1"]
    #         field_password2 = self.fields["password2"]
    #         for view in [field_password1, field_password2]:
    #             if hasattr(view, "validators"):
    #                 has_method_length = any(
    #                     isinstance(v, MinLengthValidator) for v in view.validators
    #                 )
    #                 if has_method_length:
    #                     view.validators = [
    #                         v
    #                         for v in view.validators
    #                         if not isinstance(v, MinLengthValidator)
    #                     ]
    #                     view.validators.append(
    #                         MinLengthValidator(APP_MINIMUM_PASSWORD_LENGTH)
    #                     )
    #             else:
    #                 # I won't believe if SignupForm.password* doesn't have the validators prop.
    #                 view.validators = []
    #                 view.validators.append(
    #                     MinLengthValidator(APP_MINIMUM_PASSWORD_LENGTH)
    #                 )

    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "w-field__input form-email",
                "required": True,
                "placeholder": "Email",
                "type": "email",
            },
        ),
        max_length=50,
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(50),
            EmailValidatorPerson(),
        ],
        error_messages={
            "required": _("Please enter the email address in this field."),
            "invalid": _("Please enter the valid email address in this filed."),
        },
    )

    category = forms.ChoiceField(
        choices=CATEGORY_STATUS,
        label=_("Category"),
        widget=forms.Select(
            choices=CATEGORY_STATUS,
            attrs={
                "class": "w-field__input form-status",
                "required": True,
                "placeholder": _("Select a category"),
                "type": "select",
            },
        ),
        help_text=_("Choice your status and access rights"),
        error_messages={
            "required": _("Please select a your category."),
            "invalid": _("Please enter a valid category."),
        },
    )

    first_name = forms.CharField(
        required=False,
        label=_("First Name"),
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": " w-field__input form-first-name",
                "required": False,
                "id": "id_username",
                "placeholder": _("If you want you can enter your first name."),
                "type": "text",
            }
        ),
        help_text=_("Field is not required"),
        error_messages={"invalid": _("Please enter a valid first name.")},
    )
    username_validator = UnicodeUsernameValidator()

    username = forms.CharField(
        label=_("Username"),
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(50),
        ],
        widget=forms.TextInput(
            attrs={"placeholder": _("Username"), "autocomplete": "username"}
        ),
    )
    check_user = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "w-field__input form-checkbox",
            }
        ),
        required=True,
        label=_("Data Processing Consent"),
        error_messages={
            "required": _("Please select a consent to data processing."),
            "invalid": _("Please enter a valid consent to data processing."),
        },
    )

    # check_user = RadioFieldWithHelpText(
    #     choice_help_text= _("You consent to data processing.")
    # )
    class Meta:
        model = Users
        fields = (
            "username",
            "first_name",
            "email",
            "category",
            "password1",
            "password2",
        )

    # def clean_email(self):
    #     email: str = self.cleaned_data.get("email")
    #     log.info(f"DEBUG VALIDATE EMAIL {email}: 1")
    #     if Users.objects.filter(email=email).exists():
    #         log.info(f"DEBUG VALIDATE EMAIL {email}: 2")
    #         raise forms.ValidationError(_("A user with this email already exists."))
    #     log.info(f"DEBUG VALIDATE EMAIL {email}: 3")
    #     if len(email) < 5 or len(email) > 150:
    #         raise forms.ValidationError(_("The length of name email is not valid."))
    #     return email

    def clean_dublicate_username(self):
        username = self.cleaned_data.get("username")
        if username is not None and Users.objects.filter(username=username).exists():
            return False
        return True

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        first_chars = r"[+\\}{)(0-9\"\' -.]"
        if first_name is not None and len(first_name) > 0:
            if re.match(first_chars, first_name):
                log_t = f'Please inter valid "username". Username does not must begin with {first_name[0]}'
                log.warning(log_t)
                raise forms.ValidationError(_(log_t))

            if not re.search(r"[A-Za-z]+", first_name[0:]):
                log_t = "Please enter the valid first_name. This first_name could be contain the chars: 'A-Za-z'"
                log.warning(log_t)
                raise forms.ValidationError(_(log_t))
        return first_name

    def clean_username(self):
        username = self.cleaned_data.get("username")
        first_chars = r"[+\\}{)(0-9\"\' -.]"
        if re.match(first_chars, username):
            log_t = f'Please inter valid "username". Username does not must begin with {username[0]}'
            log.warning(log_t)
            raise forms.ValidationError(_(log_t))

        if not re.search(r"[A-Za-z_0-9]+", username[0:]):
            log_t = "Please enter the valid username. Username could be contain the chars: 'A-Za-z_0-9'"
            log.warning(log_t)
            raise forms.ValidationError(_(log_t))
        return username

    def clean_password(self):
        """
        :return: Void
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not password1 or not password2:
            log_t = "Password fields were not filled."
            log.warning(log_t)
            raise forms.ValidationError(_(log_t))

        if (
            len(password1) < APP_MINIMUM_PASSWORD_LENGTH
            or password2 > APP_MAX_PASSWORD_LENGTH
        ):
            log_t = f"The length of 'password1' or 'password2' is not valid. MAX is {APP_MAX_PASSWORD_LENGTH} \
& MIN is {APP_MINIMUM_PASSWORD_LENGTH}. "
            log.warning(log_t)
            raise forms.ValidationError(_(log_t))

    def save(self, request):
        users = super().save(request)
        # Required
        email = self.cleaned_data.get("email")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        username = self.cleaned_data.get("username")
        # Email
        if not email:
            raise forms.ValidationError(_("Please enter a valid email address."))

        users.category = self.cleaned_data.get("category")
        # First name
        if first_name is not None:
            users.first_name = first_name

        # Last name
        if last_name is not None:
            users.last_name = last_name

        # User name
        if username is None:
            # 'username' required for the email auth.
            users.username = email.split("@")[0] if email is None else username

        users.is_active = False
        users.save()
        return users
