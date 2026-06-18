# catalog/models/model_product_gellary_image.py:1
# Intermediate model between product, image for product and pages of one product,
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey

from catalog.models.model_abstract import AbstractModel


class ProductGalleryImageModel(AbstractModel):
    id = models.AutoField(primary_key=True)
    page = ParentalKey("ProductPageModel", related_name="gallery_images")
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    product = models.ForeignKey(
        "ProductModel", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(
        blank=True, max_length=250, null=True, help_text=_("The caption of the image")
    )

    panels = ["image", "product", "caption"]
