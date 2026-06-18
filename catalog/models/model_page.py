# catalog/models/model_page.py:1
# IT page for product and gallery of product,

from django.db import models
from django.utils.translation import gettext_lazy as _

from .model_abstract import AbstractCategoryPage


class ProductPageModel(AbstractCategoryPage):
    id = models.AutoField(primary_key=True)

    class Meta:
        verbose_name = _("Product Page")
        db_table = "product_page_model"
