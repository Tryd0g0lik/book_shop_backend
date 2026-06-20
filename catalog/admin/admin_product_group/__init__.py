from wagtail_modeladmin.options import ModelAdminGroup, modeladmin_register

__all__ = (
    "ProductAdmin",
    "PageAdmin",
    "CategoryAdmin",
    "BrandAdmin",
    "ProductGalleryImageAdmin",
    "ProductCharacteristicsAdmin",
)

from catalog.admin.admin_product_group.admin_brand import BrandAdmin
from catalog.admin.admin_product_group.admin_category import CategoryAdmin

# Product Group
from catalog.admin.admin_product_group.admin_page import PageAdmin
from catalog.admin.admin_product_group.admin_product import ProductAdmin
from catalog.admin.admin_product_group.admin_product_characteristics import (
    ProductCharacteristicsAdmin,
)
from catalog.admin.admin_product_group.admmin_product_gallery_Image import (
    ProductGalleryImageAdmin,
)

# ---


class ProductGroup(ModelAdminGroup):
    menu_label = "Product Group"
    menu_name = "ProductGroup"
    menu_icon = "folder-invers"
    menu_order = 1000
    items = (
        ProductAdmin,
        PageAdmin,
        BrandAdmin,
        CategoryAdmin,
        ProductCharacteristicsAdmin,
        ProductGalleryImageAdmin,
    )


# register_snippet(ProductPageViewSet)
modeladmin_register(ProductGroup)
