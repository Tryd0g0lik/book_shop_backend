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
    EmailValidator,
    MaxLengthValidator,
    MinLengthValidator,
)
from django.utils.translation import gettext_lazy as _
from shtab import Optional

from persons import EnumTemplatesKeysCache
from persons.apps import cachemanager
from persons.exceptions.error_forms import ErrorCodeVerificationForm
from persons.models import Users
from persons.validators import EmailValidatorPerson

# from persons.services import CacheManager
from project.settings_conf.settings_env import (
    APP_MINIMUM_PASSWORD_LENGTH,
    CATEGORY_STATUS,
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


class UsersCheckCodeVerificationForm(UserTokenForm):
    """
    Here we get the code verification. We have sent this code to the user's email address for email configuration.
    """

    uidb36 = None

    def _get_user(self, code_token: str) -> dict:
        """
        This code look up to the cache server by the template key from the selection
            list 'EnumTemplatesKeysCache.USER_PENDING_LETTER.value'.
        Time live extending on 300000 milliseconds.
        :param str code_token:
        :return: VERIFICATION CODE or the mistake name 'ErrorCodeVerificationForm'.
        """
        # Get user from cash server
        log_t = f"[{self.__class__.__name__}][{self._get_user.__name__}]:"
        cache_key = EnumTemplatesKeysCache.USER_PENDING_LETTER.value % "*"
        collection_keys = []
        log.info(
            f"""{log_t}
        # ============================================
        # LOOK UP THE VERIFICATION CODE BY TOKEN
        # ============================================
        """
        )
        try:
            # BELOW WE GET A LIST KEYS OF CACHE
            result_bool = cachemanager.aget(
                key_pattern=cache_key, collection=collection_keys
            )
            if result_bool is not None and len(collection_keys) >= 1:
                promocodes = []
                for key_bytes in collection_keys:
                    key_str = key_bytes.decode()
                    cachemanager.aget(key=key_str, collection=promocodes)
                # BELOW WE GET A LIST OF JSON BYTES
                for view_bytes in promocodes:
                    view_json: dict = json.loads(view_bytes.decode())
                    # BELOW WE GET VALUES & LOOK UP THE VERIFICATION TOKEN IN HIM
                    verification_code: Optional[str] = view_json.get(
                        "verification_code"
                    )
                    if (
                        verification_code is not None
                        and verification_code == code_token
                    ):
                        promocodes.clear()
                        k = re.sub(
                            r"[@.]+", "", (cache_key[:-1] + view_json.get("email"))
                        )
                        cachemanager.aget(key=k, collection=promocodes, ex=300000)
                        # THE CODE VERIFICATION WAS FOUND & THE USER JSON DATA WE RETURN

                        return view_json

            raise ErrorCodeVerificationForm("Code verification invalid.")
        except Exception as e:
            raise ErrorCodeVerificationForm(e.args[0] if e.args else str(e)) from e

    def clean(self) -> dict:
        """
        TODO: Checking logic
        :return:
        """
        cleaned_data = super().clean()
        code_token = cleaned_data.get("code_token")

        if not code_token:
            raise ErrorCodeVerificationForm("Code was not found")
        try:
            result_json: dict = self._get_user(code_token)
            return result_json
        except Exception as e:
            raise e
