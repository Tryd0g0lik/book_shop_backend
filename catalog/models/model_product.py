# catalog/models/model_product.py:20
# Model of Product
from decimal import Decimal

from allauth.account.models import EmailAddress
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
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.fields import RichTextField

from .model_abstract import AbstractModel

# from wagtail.images.image_operations import


class ProductModel(AbstractModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=80,
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(80),
        ],
        unique=True,
        help_text=_("The name of the product"),
        db_index=True,
    )
    describe_preview = RichTextField(
        null=True,
        blank=True,
        help_text=_("The preview description of the product"),
        validators=[
            MaxLengthValidator(150),
        ],
        features=["bold", "italic", "link", "ol", "ul", "image", "embed"],
    )

    description = RichTextField(
        null=True,
        blank=True,
        help_text=_("The description of the product"),
        validators=[
            MaxLengthValidator(1000),
        ],
        features=["bold", "italic", "link", "ol", "ul", "image", "embed"],
    )
    category = models.ForeignKey(
        "CategoryModel",
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("The category of the product"),
        db_index=True,
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
            DecimalValidator(max_digits=10, decimal_places=2),
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
            DecimalValidator(max_digits=4, decimal_places=2),
        ],
        help_text=_("The discount percentage of the product"),
    )
    stock_quantity = models.IntegerField(
        default=0,
        help_text=_("The quantity of the product"),
        db_index=True,
    )
    attributes = models.ForeignKey(
        "ProductCharacteristics",
        help_text=_("Commons characteristics of the ont product."),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="+",
    )
    attributes_additional = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text=_("Uniquer (for product) characteristics of the one product."),
    )

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        "is_active",
                        "name",
                        FieldPanel("created_at", read_only=True),
                    ]
                ),
                FieldRowPanel(
                    [
                        "category",
                        "brand",
                    ]
                ),
                FieldRowPanel(
                    [
                        "price",
                        "stock_quantity",
                        "discount_percent",
                    ]
                ),
                "describe_preview",
                "description",
                PageChooserPanel("attributes"),
                "attributes_additional",
            ]
        ),
    ]

    class Meta:
        verbose_name = _("Product")
        db_table = "product_model"
        unique_together = (("name", "category"), ("name", "brand"))

    def __str__(self):
        return f"{self.name} - {self.created_at}"

    # def clean_descriptions(self):
    #     if self.description is not None:
    #         if self.description > 0 and (
    #             self.describe_preview is None or self.describe_preview == 0
    #         ):
    #             max_length = self.describe_preview
    #             self.describe_preview = self.description[: max_length - 4]
    #
    #             self.describe_preview = (
    #                 self.describe_preview[: max_length - 4] + " ..."
    #                 if len(self.describe_preview) == max_length
    #                 else self.describe_preview
    #             )

    def clean_price(self):
        if self.price is None or self.price < 0:
            self.price = 0

    def clean_attributes_additional(self):
        if self.attributes_additional is None:
            pass

    def clean(self):
        super().clean()

    def save(
        self,
        *,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):

        if update_fields:
            pass
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    # def clean_discount(self):
    #     if (
    #         (self.discount_percent is None or int(self.discount_percent) < 0)
    #         if type(self.discount_percent) in (str,)
    #         else self.discount_percent < 0
    #     ):
    #         self.discount_percent = 0
