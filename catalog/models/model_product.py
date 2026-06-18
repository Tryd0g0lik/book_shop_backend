# catalog/models/model_product.py:20
# Model of Product
from decimal import Decimal

from django.core.validators import (
    DecimalValidator,
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.fields import RichTextField
from wagtail.images.models import Image

from catalog.models.model_abstract import AbstractModel

# from wagtail.images.image_operations import


class ProductModel(AbstractModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=80,
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(80),
            RegexValidator(r"[\w., \-_]{3:100}"),
        ],
        unique=True,
        help_text=_("The name of the product"),
    )
    describe_preview = RichTextField(
        null=True,
        blank=True,
        help_text=_("The preview description of the product"),
        validators=[MaxLengthValidator(150), RegexValidator(r"[\w., \-_]{0:150}")],
        features=["bold", "italic", "link"],
    )

    description = RichTextField(
        null=True,
        blank=True,
        help_text=_("The description of the product"),
        validators=[
            MaxLengthValidator(1000),
            RegexValidator(r"[\w., \-_]{0:150}"),
        ],
        features=["bold", "italic", "link", "ol", "ul", "image", "embed"],
    )
    category = models.ForeignKey(
        "CategoryModel",
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("The category of the product"),
    )
    brand = models.ForeignKey(
        "BrandModel",
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("The brand of the product"),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("99999999.99")),
            DecimalValidator(),
        ],
        help_text=_("The price of the product"),
    )
    discount_percent = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("99.99")),
            DecimalValidator(),
        ],
        help_text=_("The discount percentage of the product"),
    )
    stock_quantity = models.IntegerField(
        default=0, help_text=_("The quantity of the product")
    )

    panels = ["__all__"]

    def clean_descriptions(self):
        if self.description is not None:
            if len(self.description) > 0 and (
                self.describe_preview is None or len(self.describe_preview) == 0
            ):
                max_length = self.describe_preview.max_length
                self.describe_preview = self.description[: max_length - 4]

                self.describe_preview = (
                    self.describe_preview[: max_length - 4] + " ..."
                    if len(self.describe_preview) == max_length
                    else self.describe_preview
                )

    def clean_price(self):
        if self.price is None or self.price < 0:
            self.price = 0

    def clean_discount(self):
        if (
            (self.discount_percent is None or int(self.discount_percent) < 0)
            if type(self.discount_percent) in (str,)
            else self.discount_percent < 0
        ):
            self.discount_percent = 0
