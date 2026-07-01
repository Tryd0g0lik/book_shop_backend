# catalog/admin/admin_product_group/admmin_product_gallery_Image.py:1

from django import forms
from django.forms import Select, TextInput
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from catalog.models import ProductGalleryImageModel


class ProductGalleryImageAdmin(ModelAdmin):
    """Every position contain (in self) it and a product data, and images fot product
    This is the middle table between the table (models):
    - images gallery (of wagtail) for products;
    - products positions;
    - characteristics of products. It is a common properties which we often can see in between positions;
    And additional descript.
    """

    model = ProductGalleryImageModel
    icon = "tag"
    menu_icon = "tag"
    menu_label = _("Pages of products")
    menu_item_name = _("Catalog_item_name")
    menu_item_title = _("Catalog_item_title")
    base_url_path = "catalog/products"
    menu_order = 1002
    add_to_admin_menu = False

    list_display = [
        "is_active",
        "caption",
        "product",
        "version",
        "published_at",
        "id",
    ]

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("version", read_only=True),
                        FieldPanel(
                            "is_active",
                            widget=forms.CheckboxInput(attrs={"required": False}),
                        ),
                    ]
                ),
                FieldPanel("page"),
                FieldPanel("product", widget=Select(attrs={"class": "selectpicker"})),
                # FieldPanel("product_characteristic"),
                FieldPanel("caption"),
                FieldRowPanel(
                    [
                        FieldPanel("created_at", read_only=True),
                        FieldPanel("updated_at", read_only=True),
                        FieldPanel("published_at", read_only=True),
                    ]
                ),
                # InlinePanel(
                #     "properties",
                #     heading=_("Properties"),
                #     label=_("Property"),
                #     classname="custom-property-value",
                #     panels=[
                #         MultiFieldPanel(
                #             [
                #                 FieldRowPanel(
                #                     [
                #                         FieldPanel(
                #                             "name",
                #                             required_on_save=True,
                #                             classname="form-property-name",
                #                         ),
                #                         FieldPanel(
                #                             "value",
                #                             required_on_save=True,
                #                             widget=TextInput(
                #                                 attrs={
                #                                     "required": True,
                #                                     "name": "Characteristic-value",
                #                                 }
                #                             ),
                #                             classname="form-characteristic-value",
                #                         ),
                #                     ]
                #                 ),
                #                 "description",
                #                 FieldPanel("created_at", read_only=True),
                #                 "id",
                #             ]
                #         )
                #     ],
                # ),
                # InlinePanel(
                #     "images",  # This is the related_name from OneImageModels
                #     label=_("Image"),
                #     heading=_("Images"),
                #     classname="custom-property-value",
                #     panels=[
                #         MultiFieldPanel(
                #             [
                #                 FieldPanel("title"),
                #                 FieldPanel("image"),
                #                 FieldRowPanel(
                #                     [
                #                         FieldPanel("describe"),
                #                         FieldPanel("label"),
                #                     ]
                #                 ),
                #                 FieldRowPanel(
                #                     [
                #                         FieldPanel("x"),
                #                         FieldPanel("y"),
                #                     ]
                #                 ),
                #             ]
                #         )
                #     ],
                # ),
            ]
        ),
    ]
