# catalog/admin/admin_product_group/admmin_product_gallery_Image.py:1
from django.forms import ChoiceField, Select, SelectMultiple
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel

# from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail_modeladmin.options import ModelAdmin

from catalog.models import ProductGalleryImageModel


# class ImageChooserBlockNew(ImageChooserBlock):
#     def get_api_representation(self, value, context=None):
#         if value:
#             return {
#                 "id": value.id,
#                 "title": value.title,
#                 "original": value.get_rendition("original").attrs_dict,
#                 "thumbnail": value.get_rendition("fill-120x120").attrs_dict,
#             }
#
class ProductGalleryImageAdmin(ModelAdmin):
    model = ProductGalleryImageModel
    # add_to_admin_menu=True,
    menu_order = 400
    icon = "product"
    menu_icon = "product"
    menu_label = "Product Image Page"

    list_display = [
        "is_active",
        "caption",
        "image",
        "product",
        "version",
        "published_at",
        "id",
    ]
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("id"),
                FieldRowPanel(
                    [
                        FieldPanel("page", widget=Select, required_on_save=True),
                        FieldPanel("version", read_only=True),
                        FieldPanel("is_active"),
                    ]
                ),
                FieldPanel("published_at", read_only=True),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                FieldPanel("caption"),
                                # widget=SelectMultiple
                                FieldPanel("product", widget=Select),
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel(
                                    "image",
                                    widget=SelectMultiple,
                                    required_on_save=True,
                                ),
                            ]
                        ),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("created_at", read_only=True),
                        FieldPanel("created_by", read_only=True),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("updated_at", read_only=True),
                        FieldPanel("updated_by", required_on_save=True),
                    ]
                ),
            ]
        ),
    ]

    #
    def image_tag(self, obj):
        from django.utils.html import format_html

        return format_html(
            '<img src="{}" style="max-width:200px; max-height:200px"/>'.format(
                obj.image.url
            )
        )
