"""
persons/models/models_persons.py:1
"""

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import (
    EmailValidator,
    MaxLengthValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from project.settings_conf.settings_env import (
    APP_MAX_PASSWORD_LENGTH,
    APP_MINIMUM_PASSWORD_LENGTH,
    CATEGORY_STATUS,
)


# Create your models here.
class Users(AbstractUser):
    """
   Here is a new default table for the user's registration for project.
       Here, we add new fields for the user registration.
   :param is_activated: bool. This is activation a new account after the \
       authentication. By link from the email of User, we make authentication.
   :param is_sent: bool. This is email's message, we sent to \
       the single user. His is the new user from the registration.
   :param username: str. Max length is 150 characters. This is unique\
       name of user
   :param first_name: str or None. Max length is 150 characters.
   :param last_name: str or None. Max length is 150 characters.
   :param last_login: str or N
   one, format date-time.
   :param email: str. User email. Max length is 320 characters.
   :param is_staff: bool. Designates whether the user can log into \
       this admin site.
   :param is_active: bool. Designates whether this user should be treated \
       as active.
   :param is_superuser: bool. Designates that this user has \
       all permissions. He is the admin site and only one.
   :param  password: str. Max length of characters is 128 and min is 3.
   """

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[MinLengthValidator(2), MaxLengthValidator(50), username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _("email address"),
        max_length=150,
        unique=True,
        validators=[
            MaxLengthValidator(150),
            MinLengthValidator(5),
            EmailValidator(),
        ],
    )

    category = models.CharField(default="BASE", choices=CATEGORY_STATUS, max_length=50)
    password = models.CharField(
        _("password"),
        max_length=APP_MAX_PASSWORD_LENGTH,
        validators=[MinLengthValidator(APP_MINIMUM_PASSWORD_LENGTH)],
    )
    is_sent = models.BooleanField(
        default=False,
        verbose_name="Message was sent",
        help_text=_(
            "Part is registration of new user.It is message sending \
to user's email. User indicates his email at the registrations moment."
        ),
    )
    is_verified = models.BooleanField(_("is_verified"), default=False)
    verification_code = models.CharField(
        _("verification_code"),
        max_length=150,
        blank=True,
        null=True,
        validators=[MinLengthValidator(50)],
    )
    balance = models.FloatField(
        _("balance"),
        default=0,
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField(
        _("created_at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)

    def __str__(self):
        return "User: %s Regisrated was: %s" % (self.username, self.created_at)

    class Meta(AbstractUser.Meta):
        db_table = "person"
        ordering = [
            "-id",
        ]
        indexes = [models.Index(fields=["is_active"])]

    def clean_verification_code(self):
        """Our purpose is to make the verification codes unique. Then we will be use it how the session ID for user."""
        queryset = self.objects.filter(verification_code__exact=self.verification_code)
        if queryset.count() > 0:
            self.verification_code += f"-{queryset.count()}"
