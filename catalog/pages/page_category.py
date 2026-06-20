# catalog/pages/page_category.py:1
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page


class CategoryPage(Page):
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
    description = models.TextField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, help_text=_("The creation date")
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text=_("The last update date")
    )

    content_panels = Page.content_panels + [
        "id",
        "name",
        "description",
        "created_at",
        "updated_at",
    ]
