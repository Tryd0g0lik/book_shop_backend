# persons/forms/login_form.py:1
from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.utils.translation import gettext_lazy
from django.utils.translation import gettext_lazy as _
from wagtail.admin.forms.auth import LoginForm

from persons.models import Users
from persons.validators import EmailValidatorPerson
from project.settings_conf.settings_env import (
    APP_MAX_PASSWORD_LENGTH,
    APP_MINIMUM_PASSWORD_LENGTH,
)


class UsersLoginForm(forms.Form):
    # username = forms.CharField(
    #     label=_("Username"),
    #     validators=[
    #         MinLengthValidator(2),
    #         MaxLengthValidator(50),
    #     ],
    #     widget=forms.TextInput(
    #         attrs={"placeholder": _("Username"), "autocomplete": "username"}
    #     ),
    # )
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
    password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[
            MinLengthValidator(APP_MINIMUM_PASSWORD_LENGTH),
            MaxLengthValidator(APP_MAX_PASSWORD_LENGTH),
        ],
    )
    username = None
    remember = None

    class Meta:
        model = Users
        fields = ["email", "password"]
