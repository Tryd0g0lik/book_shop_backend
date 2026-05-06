# persons/forms/login_form.py:1
from django import forms
from django.utils.translation import gettext_lazy as _
from wagtail.admin.forms.auth import LoginForm

from persons.models import Users


class UsersLoginForm(LoginForm):
    from .users_registration_form import UsersRegistrationForm

    form_registering = UsersRegistrationForm()
    email = form_registering.fields.get("email")  # .widget.attrs.get("email")
    error_messages = {
        **LoginForm.error_messages,
        "invalid_form": _(
            "Something what wrong on the form 'persons.forms.login_form.UsersLoginForm'."
        ),
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        if "username" in self.fields:
            del self.fields["username"]
        if "password" in self.fields:
            del self.fields["password"]

    def clean(self):

        self.cleaned_data = super().clean()
        email = self.cleaned_data.get("email")

        if not email:
            raise forms.ValidationError(
                _("Please enter a valid email address."), code="invalid"
            )

        try:
            user = Users.objects.get(email=email)
            self.cleaned_data["user"] = user
        except Users.DoesNotExist as e:
            raise forms.ValidationError(
                _(
                    "No user found with this email address. Please enter a valid email address. Error: %s"
                )
                % str(e),
                code="user_not_found",
            )
        except Exception as e:
            raise forms.ValidationError(
                _("Form 'UsersLoginForm' is invalid. Error: %s") % str(e),
                code="invalid_form",
            )
        return self.cleaned_data

    @property
    def extra_fields(self):
        for field_name in self.fields.keys():
            if field_name not in [
                "email",
            ]:
                yield field_name, self[field_name]
