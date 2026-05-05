"""
persons/forms/users_registration_form.py:1
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import (
    EmailValidator,
    MaxLengthValidator,
    MinLengthValidator,
)
from django.utils.translation import gettext_lazy as _

from persons.models import Users
from project.settings_conf.settings_env import CATEGORY_STATUS


class UsersRegistrationForm(UserCreationForm):
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
        validators=[MinLengthValidator(5), MaxLengthValidator(50), EmailValidator()],
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
        max_length=150,
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

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError(_("A user with this email already exists."))
        return email

    def save(self, commit=True):
        users = super().save(commit=False)
        # Required
        email = self.cleaned_data.get("email")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        username = self.cleaned_data.get("username")
        # Email
        if not email:
            raise forms.ValidationError(_("Please enter a valid email address."))
        users.email = email
        users.category = self.cleaned_data.get("category")
        # First name
        if first_name is not None:
            users.first_name = first_name

        # Last name
        if last_name is not None:
            users.last_name = last_name

        # User name
        if username is not None:
            # 'username' required for the email auth.
            users.username = email.split("@")[0]

        if commit:
            users.save()
        return users
