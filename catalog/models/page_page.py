# catalog/models/page_page.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import InlinePanel
from wagtail.models import Page


class ProductPage(Page):
    name = models.CharField(
        max_length=80,
    )
    description = models.TextField(max_length=250, null=True, blank=True)
    created_at = models.DateField(help_text=_("The creation date"))
    updated_at = models.DateField(help_text=_("The last update date"))

    content_panels = Page.content_panels + [
        "name",
        "description",
        "created_at",
        "updated_at",
    ]


content_panels = Page.content_panels + [
    # ... другие панели
    InlinePanel("gallery_images", label="Gallery Images"),
]
