# catalog/models/model_product_gellary_image.py:1
# Intermediate model between product, image for product and pages of one product,
# from allauth.account.models import EmailAddress
from django.db import models
from django.utils.translation import gettext_lazy as _

from catalog.models.model_abstract import AbstractModel


class ProductGalleryImageModel(AbstractModel):
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

    # panels = [Image("image"), "product", "caption"]

    class Meta:
        verbose_name = _("Product Gallery Image")
        verbose_name_plural = _("Product Gallery Images")
        ordering = ["-created_at"]
        db_table = "product_gallery_image"
        unique_together = (("page", "product"),)
