# catalog/models/model_bstract.py:1
# from allauth.account.models import EmailAddress
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, help_text=_("The creation date")
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text=_("The last update date")
    )
    created_by = models.ForeignKey(
        "profiles.UserProfileManagerModel",
        on_delete=models.SET_NULL,
        help_text=_("THe user who created the position"),
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_product_characteristics_created",
        db_comment="""This is a user's profile created position. Just that is goes not to the direct user. That is go to
        the profile user: 'UserProfileManagerModel' => \
        'profiles.models.model_<client | admin | editor | manager | client| moderator >' => \
        'wagtail.users.models.UserProfile' => 'persons.models.Users' model.
        If need  a direct user mean we get of user through the 'ProfilesModel' model..
        """,
    )
    updated_by = models.ForeignKey(
        "profiles.UserProfileManagerModel",
        on_delete=models.SET_NULL,
        help_text=_("The user who last updated the position"),
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_product_characteristics_updated",
        db_comment="""This is a user last updated position.
        If need a direct user mean we act by analogy the 'self.created_by """,
    )
    is_active = models.BooleanField(
        default=False, help_text=_("Designates whether this item is used or not")
    )

    class Meta:
        abstract = True
        ordering = ["-updated_at"]

    # created_by


class AbstractCategoryPage(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    name = models.CharField(
        max_length=80,
        unique=True,
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(80),
            RegexValidator(r"^[\w \-_]{3,80}$"),
        ],
        help_text=_("The name of the category"),
    )
    description = models.TextField(
        max_length=250,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text=_("The creation date")
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text=_("The last update date")
    )

    class Meta:
        abstract = True
        ordering = ("-name",)
