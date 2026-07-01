# catalog/admin/admin_product_group/admin_product.py:1
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from wagtail_modeladmin.options import ModelAdmin

from catalog.models import ProductModel


class ProductAdmin(ModelAdmin):
    model = ProductModel
    menu_icon = "tag"
    menu_label = _("Products")
    add_to_settings_menu = True
    exclude_from_explorer = False
    base_url_path = "catalog/product"
    menu_order = 500
    list_per_page = 25
    list_display = [
        "id",
        "name",
        "category",
        "brand",
        "price",
        "stock_quantity",
        "is_active",
    ]
    search_fields = ["name", "brand", "category"]
