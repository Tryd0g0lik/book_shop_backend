# catalog/models/model_produt_characteristics.py:1

from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.db import models
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel

from catalog.models.model_abstract import AbstractCategoryPage


class ProductCharacteristics(AbstractCategoryPage):
    """
    TODO: Тут общие наименования характеристик продукта
        value - поле для характеристик. Написать валидатор который определяе
        строковые данные или числовые. Если числа то не забыть! есть десятичные и с плавающей точкой.

    """

    name = models.CharField(
        max_length=80,
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(80),
            RegexValidator(r"^[\w \-_]{3,80}$"),
        ],
        help_text=_("The name of the property"),
        db_index=True,
    )
    value = models.CharField(
        default="-",
        max_length=10,
        validators=[MaxLengthValidator(10)],
        help_text=_("The value of the property"),
    )
    product = ParentalKey(
        "ProductModel",
        help_text=_("Commons characteristics of the ont product."),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="product Characteristics",
        related_name="characteristics",
    )

    class Meta:
        db_table = "product_characteristics"
        verbose_name_plural = "Product Characteristics"
        unique_together = (("name", "value"),)
        ordering = ["name"]
        verbose_name = "Product Characteristic"

    def __str__(self):
        return f"{self.name} - {self.value}"
