# catalog/models/model_product_gallery_image.py:1
# Intermediate model between product, image for product and pages of one product,
# from allauth.account.models import EmailAddress
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from catalog.models.model_abstract import AbstractModel


class ProductGalleryImageModel(AbstractModel):
    f"""
    It is a set of content for publish.
    Every item it is one page.
    Every page would be to contain the one product:
        1. The product, it is a page  that have a general content obout product
        2. The page contain a publish title and additional info.
        3. The images.
    :param {bool} is_active: Designates will be used or this page will be simply not active.
    :param {str} caption: It is one general for all images of product which contain on this page.
    :param {str} version: Quantity of changes. By default, it is 0.
        Every saves this page will be add else number.
    """
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(
        "ProductPageModel",
        related_name="+",
        on_delete=models.CASCADE,
        limit_choices_to={"is_active": True},
    )
    # image = models.ForeignKey(
    #     "wagtailimages.Image",
    #     on_delete=models.CASCADE,
    #     limit_choices_to={},
    #     related_name="+",
    #
    # )
    image = models.ManyToManyField(
        "wagtailimages.Image",
        limit_choices_to={},
        related_name="+",
        related_query_name="image_query_related",
    )
    product = models.ForeignKey(
        "ProductModel",
        on_delete=models.CASCADE,
        related_name="+",
        limit_choices_to={"is_active": True},
        related_query_name="product_related",
    )
    caption = models.CharField(
        blank=True, max_length=250, null=True, help_text=_("The caption of the image")
    )
    version = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        null=True,
        help_text=_("The version of changing the product"),
    )
    is_active = models.BooleanField(
        default=False, help_text=_("Designates whether this item is active.")
    )
    published_at = models.DateTimeField(
        null=True, blank=True, help_text=_("Designates when this item was published")
    )
    # panels = [
    #     FieldPanel("caption"),
    #     FieldPanel("image"),
    #     FieldPanel("product"),
    #     FieldPanel("version"),
    #     FieldPanel("is_active"),
    #     FieldPanel("published_at", read_only=True),
    #     FieldPanel("updated_by", required_on_save=True),
    # ]
    # panels = [Image("image"), "product", "caption"]

    class Meta:
        verbose_name = _("Product Gallery Image")
        verbose_name_plural = _("Product Gallery Images")
        ordering = ["-created_at"]
        app_label = "catalog"
        db_table = "product_gallery_image"
        unique_together = (("page", "product"),)

    def __str__(self):
        return f"Page {self.page.name} - Product: {self.product.name}"

    def clean_version(self) -> None:
        if self.version < 0 and self.version == 9999:
            self.version = 0
            self.save(update_fields=["version"])
        else:
            self.version += 1
            self.save(update_fields=["version"])

    def save(
        self,
        *,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ) -> None:
        from wagtail.images.views.images import Image

        if self.is_active:
            controller = False
            if self.version == 0:
                controller = True
            elif (
                isinstance(update_fields, list | tuple)
                and self.is_active.__name__ not in update_fields
            ):
                update_fields.append(self.published_at.__name__)
                controller = True

            if controller:
                self.published_at = datetime.now()
        elif not self.is_active and (
            isinstance(update_fields, list | tuple)
            and self.is_active.__name__ not in update_fields
        ):
            self.published_at = None
        else:
            if (
                isinstance(update_fields, list | tuple)
                and self.is_active.__name__ not in update_fields
            ):
                del update_fields[self.published_at.__name__]
                # self.published_at = None
        super().save(
            using=using,
            force_insert=force_insert,
            force_update=force_update,
            update_fields=update_fields,
        )
