# catalog/models/model_bstract.py:1
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
        "EmailAddress",
        on_delete=models.SET_NULL,
        help_text=_("THe user who created the position"),
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "EmailAddress",
        on_delete=models.SET_NULL,
        help_text=_("The user who last updated the position"),
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ["-updated_at"]


class AbstractCategoryPage(AbstractModel):
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

    class Meta:
        abstract = True
