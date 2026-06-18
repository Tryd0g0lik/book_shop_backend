# catalog/models/model_page.py:1
# IT page for product and gallery of product,

from django.db import models

from catalog.models.model_abstract import AbstractModel


class ProductPageModel(AbstractModel):
    id = models.AutoField(primary_key=True)
