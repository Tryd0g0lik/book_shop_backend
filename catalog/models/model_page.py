# catalog/models/model_page.py:1
# IT page for product and gallery of product,

from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel

from .model_abstract import AbstractCategoryPage


class ProductPageModel(AbstractCategoryPage):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=False, verbose_name=_("Is active?"))
    # panels = [
    #     FieldPanel("id"),
    #     MultiFieldPanel([
    #         FieldRowPanel([
    #             FieldPanel("name"),
    #             FieldPanel("created_at"),
    #             FieldPanel("is_active"),
    #         ])
    #     ]),
    #
    #     FieldPanel("description"),
    #
    #     FieldPanel("updated_at", required_on_save=True),
    # ]

    class Meta:
        verbose_name = _("Product Page")
        db_table = "product_page_model"

    def __str__(self):
        return f"Page: {self.name}"
