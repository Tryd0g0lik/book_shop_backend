# catalog/models/model_produt_characteristics.py:1
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from catalog.models.model_abstract import AbstractCategoryPage


class ProductCharacteristics(AbstractCategoryPage):
    """
    TODO: Тут общие наименования характеристик продукта
        value - поле для характеристик. Написать валидатор который определяе
        строковые данные или числовые. Если числа то не забыть! есть десятичные и с плавающей точкой.

    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=80,
        unique=True,
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(80),
            RegexValidator(r"^[\w \-_]{3,80}$"),
        ],
        help_text=_("The name of the category"),
        db_index=True,
    )
    value = models.CharField(
        default="-", max_length=10, validators=[MaxLengthValidator(10)]
    )

    class Meta:
        db_table = "product_characteristics"
        verbose_name_plural = "Product Characteristics"
        ordering = ["name"]
        verbose_name = "Product Characteristic"
