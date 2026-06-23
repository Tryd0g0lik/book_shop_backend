# # catalog/models/model_schematic_points.py:2
# from django import forms
# from django.core.validators import MaxValueValidator, MinValueValidator
# from django.db import models
# from modelcluster.fields import ParentalKey
# from wagtail.admin.panels import FieldPanel
# from wagtail.models import Orderable
#
#
# class SchematicPoint(Orderable, models.Model):
#     schematics = ParentalKey(
#         "SchematicModel", on_delete=models.CASCADE, related_name="points"
#     )
#     label = models.CharField("label", max_length=254)
#     x = models.DecimalField(
#         verbose_name="X ->",
#         max_digits=5,
#         decimal_places=2,
#         default=0.0,
#         validators=[MaxValueValidator(100.0), MinValueValidator(0.0)],
#     )
#
#     y = models.DecimalField(
#         verbose_name="Y ↑",
#         max_digits=5,
#         decimal_places=2,
#         default=0.0,
#         validators=[MaxValueValidator(100.0), MinValueValidator(0.0)],
#     )
#     panels = [
#         FieldPanel("schematics"),
#         FieldPanel("label"),
#         FieldPanel(
#             "x",
#             widget=forms.NumberInput(attrs={"min": 0.0, "max": 100.0}),
#             classname="x",
#         ),
#         FieldPanel(
#             "y",
#             widget=forms.NumberInput(attrs={"min": 0.0, "max": 100.0}),
#             classname="y",
#         ),
#     ]
#
#     def __str__(self):
#         schematic_title = getattr(self, "title", "SchematicModel")
#
#         return f"Schematic - {schematic_title} ({self.label})"
#
#     class Meta:
#         verbose_name = "Point"
#         verbose_name_plural = "Points"
