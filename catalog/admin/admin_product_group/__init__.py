# catalog/admin/admin_product_group/__init__.py:2

from wagtail_modeladmin.options import ModelAdminGroup, modeladmin_register

__all__ = (
    "CategoryAdmin",
    "BrandAdmin",
    "ProductGalleryImageAdmin",
    "OneImageAdmin",
    "ProductAdmin",
    "CharacteristicsAdmin",
)

# Product Group
from catalog.admin.admin_product_group.admin_brand import BrandAdmin
from catalog.admin.admin_product_group.admin_category import CategoryAdmin
from catalog.admin.admin_product_group.admin_characteristics import CharacteristicsAdmin
from catalog.admin.admin_product_group.admin_one_image import OneImageAdmin
from catalog.admin.admin_product_group.admin_product import ProductAdmin
from catalog.admin.admin_product_group.admmin_product_gallery_Image import (
    ProductGalleryImageAdmin,
)


@modeladmin_register
class ProductGroup(ModelAdminGroup):
    menu_label = "Catalog"
    menu_name = "Catalog"
    menu_icon = ("folder-open-inverse",)  # "folder-invers"
    add_to_admin_menu = True

    menu_order = 1000
    items = (
        BrandAdmin,
        CategoryAdmin,
        OneImageAdmin,
        ProductAdmin,
        CharacteristicsAdmin,
        ProductGalleryImageAdmin,
    )
