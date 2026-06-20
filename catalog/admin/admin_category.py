# catalog/admin/admin_category.py:1
from wagtail.admin.panels import FieldPanel
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from catalog.models import (
    BrandModel,
    CategoryModel,
    ProductGalleryImageModel,
    ProductModel,
)

# class LastnameField(Orderable):
#     user_id = ParentalKey("EmailAddress", on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_product_characteristics_updated")

#
# def describe_preview_preview(self):
#     """Короткий превью для списка"""
#     if self.describe_preview_preview:
#         return self.describe_preview_preview[:12] + "..."
#     return "-"
#
#
# describe_preview_preview.short_description = "Preview"
#
#
# def description_preview(self):
#     """Короткий превью для списка"""
#     if self.description_preview:
#         return self.description_preview[:10] + "..."
#     return "-"
#
#
# description_preview.short_description = "Description"
#
#
# class ProductPageAdmin(ModelAdmin):
#     model = ProductGalleryImageModel
#     list_display = [
#         "page",
#         "caption",
#         "image",
#         "product",
#         "version",
#         "published_at",
#     ]
#     search_fields = ["page", "caption"]
#     list_filter = ["created_at"]
#     icon = "tag"
#     add_to_admin_menu = True
#     menu_label = "Produсt Page"
#     menu_order = 300
#
#     panels = [
#         FieldPanel("page"),
#         FieldPanel("caption"),
#         FieldPanel("image"),
#         FieldPanel("product"),
#         FieldPanel("version"),
#         FieldPanel("is_active"),
#         FieldPanel("published_at", read_only=True),
#     ]
#
#
# modeladmin_register(ProductPageAdmin)
#
