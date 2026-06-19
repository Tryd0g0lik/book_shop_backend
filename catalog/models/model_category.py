# catalog/models/models_category.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel

from catalog.models.model_abstract import AbstractCategoryPage


class CategoryModel(AbstractCategoryPage):

    class Meta:
        verbose_name = _("Category")
        db_table = "category"
        app_label = "catalog"

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("created_at"),
        FieldPanel("updated_at"),
    ]

    def __str__(self):
        return self.name


class BrandModel(AbstractCategoryPage):

    class Meta:
        verbose_name = _("Brand")
        db_table = "brand"
        app_label = "catalog"

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("created_at"),
        # FieldPanel("updated_at"),
    ]

    def __str__(self):
        return self.name

    def save(self, request, obj, form, change):
        if change:
            obj.update_by = request.user.username
        super().save()
