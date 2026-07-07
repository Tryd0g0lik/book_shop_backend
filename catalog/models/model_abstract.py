# catalog/models/model_bstract.py:1
from datetime import datetime

# from allauth.account.models import EmailAddress
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel

from project.settings_conf.settings_first import DATETIME_FORMAT


class AbstractModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, help_text=_("The creation date")
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text=_("The last update date")
    )
    created_by = models.ForeignKey(
        "account.EmailAddress",
        on_delete=models.SET_NULL,
        help_text=_("THe user who created the position"),
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_product_characteristics_created",
    )
    updated_by = models.ForeignKey(
        "account.EmailAddress",
        on_delete=models.SET_NULL,
        help_text=_("The user who last updated the position"),
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_product_characteristics_updated",
    )
    is_active = models.BooleanField(
        default=False, help_text=_("Designates whether this item is used or not")
    )

    class Meta:
        abstract = True
        ordering = ["-updated_at"]


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
