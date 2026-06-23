# # catalog/models/model_schematic.py:1
# from django.db import models
# from modelcluster.models import ClusterableModel
# from wagtail.admin.panels import FieldPanel, InlinePanel
# from wagtail.images.widgets import AdminImageChooser
# from wagtail.search import index
# from wagtail.snippets.models import register_snippet
#
# from catalog.models.model_abstract import AbstractCategoryPage
#
# # from wagtail_modeladmin.options import modeladmin_register
#
#
# @register_snippet
# class SchematicModel(index.Indexed, ClusterableModel, AbstractCategoryPage):
#     name = None
#     title = models.CharField(
#         max_length=255, verbose_name="Title", help_text="The title of the schematic"
#     )
#     image = models.ForeignKey(
#         "wagtailimages.Image",
#         on_delete=models.CASCADE,
#         limit_choices_to={},
#         related_name="+",
#         related_query_name="image_%(app_label)s_%(class)s_related",
#     )
#
#     panels = [
#         FieldPanel("title"),
#         FieldPanel("image", widget=AdminImageChooser),
#         InlinePanel("points", heading="Points", label="Point"),
#     ]
#
#     def __str__(self):
#         title = getattr(self, "title", "SchematicModel")
#         return f"Schematic - {title} ({self.pk})"
#
#     class Meta:
#         verbose_name = "Schematic"
#         verbose_name_plural = "Schematics"
