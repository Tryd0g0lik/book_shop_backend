# catalog/models/models_category.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel

from catalog.models.model_abstract import AbstractCategoryPage


class CategoryModel(AbstractCategoryPage):

    class Meta:
        verbose_name = _("Category")
        db_table = "category"
        app_label = "catalog"
        ordering = ("name",)

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("created_at", read_only=True),
        FieldPanel("updated_at", read_only=True),
    ]

    def __str__(self):
        return self.name


class BrandModel(AbstractCategoryPage):

    class Meta:
        verbose_name = _("Brand")
        db_table = "brand"
        app_label = "catalog"
        ordering = ("name",)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("description"),
                FieldRowPanel(
                    [
                        FieldPanel("created_at", read_only=True),
                        FieldPanel("updated_at"),
                    ]
                ),
            ]
        ),
    ]

    def __str__(self):
        return self.name
