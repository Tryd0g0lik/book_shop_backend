# catalog/admin/admin_product_group/admin_page.py:1
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel

# from wagtail.snippets.models import register_snippet
# from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail_modeladmin.options import ModelAdmin

from catalog.models import ProductPageModel


class PageAdmin(ModelAdmin):
    model = ProductPageModel
    icon = "title"
    menu_icon = "title"
    menu_order = 100
    menu_label = _("Page")
    list_display = [
        "is_active",
        "name",
        "description",
        "created_at",
        "id",
    ]
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("id", read_only=True),
                FieldRowPanel(
                    [
                        FieldPanel("name"),
                        FieldPanel("created_at", read_only=True),
                        FieldPanel("is_active"),
                    ]
                ),
            ]
        ),
        FieldPanel("description"),
    ]


# register_snippet(PageViewSet)
