from wagtail.admin.panels import FieldPanel
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from catalog.models.images.model_image_one_item import OneImageModels


class OneImageAdmin(ModelAdmin):
    model = OneImageModels
    menu_label = "Images"
    menu_item_name = "Images"
    menu_item_title = "Images"
    menu_order = 1001
    add_to_admin_menu = True
    menu_icon = "image"
    list_display = ["title", "image", "describe"]
    search_fields = ["title", "describe"]

    # panels = [
    #     FieldPanel("title"),
    #     FieldPanel("image"),
    #     FieldPanel("describe"),
    #     FieldPanel("label"),
    #     FieldPanel("x"),
    #     FieldPanel("y"),
    #     FieldPanel("product"),  # This will show the parent relation
    # ]


modeladmin_register(OneImageAdmin)
