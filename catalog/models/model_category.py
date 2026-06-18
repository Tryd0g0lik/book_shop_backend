# catalog/models/models_category.py:1
from django.db import models
from django.utils.translation import gettext_lazy as _

from catalog.models.model_abstract import AbstractCategoryPage


class CategoryModel(AbstractCategoryPage):

    class Meta:
        verbose_name = _("Category")
        db_table = "category"
        app_label = "catalog"


class BrandModel(AbstractCategoryPage):

    class Meta:
        verbose_name = _("Brand")
        db_table = "brand"
        app_label = "catalog"
