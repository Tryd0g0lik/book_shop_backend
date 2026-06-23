# catalog/admin/admin_product_group/admin_product_test.py:1
# delete
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

#
#
# class ProductPageTestMy(Page):
#     schematic = models.ForeignKey(
#         "SchematicModel",
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name="product_page_schematic",
#     )
#
#     def get_schematic_title(self):
#         return self.schematic.title if self.schematic else "-"
#
#     get_schematic_title.short_description = "Schematic"
#
#     content_panels = Page.content_panels + [FieldPanel("schematic")]
