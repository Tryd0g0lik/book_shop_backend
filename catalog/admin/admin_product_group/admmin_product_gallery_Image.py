# catalog/admin/admin_product_group/admmin_product_gallery_Image.py:1

from django import forms
from django.forms import CheckboxInput, Select, SelectMultiple, TextInput
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.admin.telepath import register as register_telepath_adapter
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
    icon = "product"
    menu_icon = "product"
    menu_label = _("Catalog")
    menu_item_name = _("Catalog_item_name")
    menu_item_title = _("Catalog_item_title")
    menu_order = 1002
    add_to_admin_menu = True

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
                InlinePanel(
                    "properties",
                    heading=_("Properties"),
                    label=_("Property"),
                    classname="custom-property-value",
                    panels=[
                        MultiFieldPanel(
                            [
                                FieldRowPanel(
                                    [
                                        FieldPanel(
                                            "name",
                                            required_on_save=True,
                                            classname="form-property-name",
                                        ),
                                        FieldPanel(
                                            "value",
                                            required_on_save=True,
                                            widget=TextInput(
                                                attrs={
                                                    "required": True,
                                                    "name": "Characteristic-value",
                                                }
                                            ),
                                            classname="form-characteristic-value",
                                        ),
                                    ]
                                ),
                                "description",
                                FieldPanel("created_at", read_only=True),
                                "id",
                            ]
                        )
                    ],
                ),
                InlinePanel(
                    "images",  # This is the related_name from OneImageModels
                    label=_("Image"),
                    heading=_("Images"),
                    classname="custom-property-value",
                    panels=[
                        FieldPanel("title"),
                        FieldPanel("image"),
                        FieldPanel("describe"),
                        FieldPanel("label"),
                        FieldPanel("x"),
                        FieldPanel("y"),
                    ],
                ),
            ]
        ),
    ]
    # class Media:
    #     js = ("scripts/wagtail_admin_js.js",)
    # def image_tag(self, obj):
    #     """
    #     TODO: Track and verify. It doesn't seem to be doesn't working!!
    #     """
    #     from django.utils.html import format_html
    #
    #     return format_html(
    #         '<img src="{}" style="max-width:200px; max-height:200px"/>'.format(
    #             obj.image.url
    #         )
    #     )


modeladmin_register(ProductGalleryImageAdmin)


#
# class AdminPreviewImageChooser(AdminImageChooser):
#     """
#     Generates a larger version of the AdminImageChooser
#     Currently limited to showing the large image on load only.
#     """
#
#     def get_value_data(self, value):
#         value_data = super().get_value_data(value)
#
#         if value_data:
#             image = self.image_model.objects.get(pk=value_data["id"])
#             # note: the image string here should match what is used in the template
#             preview_image = image.get_rendition("width-1920")
#             value_data["preview"] = {
#                 "width": preview_image.width,
#                 "height": preview_image.height,
#                 "url": preview_image.url,
#             }
#
#         return value_data
