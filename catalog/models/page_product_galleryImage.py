# catalog/models/page_product_galleryImage.py:6
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet


class ProductGalleryImagePage(Orderable):
    page = ParentalKey(
        "ProductPage", on_delete=models.CASCADE, related_name="gallery_images"
    )
    caption = models.CharField(max_length=250, blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    product = models.ForeignKey(
        "ProductModel", on_delete=models.SET_NULL, null=True, blank=True
    )

    panels = [
        FieldPanel("caption"),
        FieldPanel("caption"),
        FieldPanel("image"),
        FieldPanel("product"),
    ]


register_snippet(ProductGalleryImagePage)
