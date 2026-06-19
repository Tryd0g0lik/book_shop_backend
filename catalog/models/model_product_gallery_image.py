# catalog/models/model_product_gellary_image.py:1
# Intermediate model between product, image for product and pages of one product,
# from allauth.account.models import EmailAddress
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel

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
        "ProductPageModel", related_name="gallery_images", on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=_("The image"),
    )
    product = models.ForeignKey(
        "ProductModel", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(
        blank=True, max_length=250, null=True, help_text=_("The caption of the image")
    )
    version = models.IntegerField(
        default=0,
        max_length=4,
        null=True,
        help_text=_("The version of changing the product"),
    )
    is_active = models.BooleanField(
        default=False, help_text=_("Designates whether this item is active.")
    )

    panels = [
        FieldPanel("caption"),
        FieldPanel("image"),
        FieldPanel("product"),
        FieldPanel("version"),
    ]
    # panels = [Image("image"), "product", "caption"]

    class Meta:
        verbose_name = _("Product Gallery Image")
        verbose_name_plural = _("Product Gallery Images")
        ordering = ["-created_at"]
        db_table = "product_gallery_image"
        unique_together = (("page", "product"),)

    def clean_version(self) -> None:
        if self.version < 0 and self.version == 9999:
            self.version = 0
            self.save()
        self.version += 1
