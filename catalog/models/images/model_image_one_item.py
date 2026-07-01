# catalog/models/images/model_image_one_item.py:1
from django import forms
from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.images.widgets import AdminImageChooser
from wagtail_modeladmin.options import modeladmin_register


# @modeladmin_register
class OneImageModels(models.Model):
    f"""
    Item for one image & additional this image hase a title and short description.
    Available char: 'A-Za-z0-9. "'_%+-'.
    Plus. Often us need use an additional data from the html code. Here using data of percent.
        Example'<img data-..="80" data-y="30"'>'. It is '80%' & '30%'.
        This data we can keep to the 'x' and 'y' of database. This data exclusively for frontend.
    :param {str} title: Min 3 & Max 100 characters. Min: 3, Max: 100.
    :param {int} image: It contain an index of image from the admin/wagtail gallery.
    :param {str} describe: The short description (or null) of the image. Min: 0, Max: 80.
    :param {str} label: Ii is header/label of below data. Default is 'label'. Min: 5, Max: 25.
    :param {float} x: The x value of percent for image. Default it hase 0.0. Min: 0.0 Max: 100.0
    :param {float} y: The x value of percent for image. Default it hase 0.0. Min: 0.0 Max: 100.0
    """
    title: str = models.CharField(
        max_length=100,
        verbose_name="Title",
        unique=True,
        help_text=r"The title of the schematic. Available char: 'A-Za-z0-9\. \"'_%+-'",
        validators=[
            MaxLengthValidator(100),
            MinLengthValidator(3),
            RegexValidator(
                regex=r"^[A-Za-z0-9\. \"'_%+-]+$",
            ),
        ],
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        limit_choices_to={},
        related_name="+",
        related_query_name="image_%(app_label)s_%(class)s_related",
    )
    product = ParentalKey(
        "catalog.ProductGalleryImageModel",
        related_name="images",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        # related_query_name="image_query_related",
    )
    describe: str = models.TextField(
        max_length=80,
        blank=True,
        null=True,
        help_text=r"The short description of the image/ Available char: 'A-Za-z0-9\. \"'_%+-'",
        validators=[
            MaxLengthValidator(80),
            RegexValidator(
                regex=r"^[A-Za-z0-9\. \"'_%+-]*$",
            ),
        ],
    )
    label: str = models.CharField(
        max_length=25,
        default="label",
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(25),
            RegexValidator(
                regex=r"^[A-Za-z0-9\. \"'_%+-]+$",
            ),
        ],
    )
    x: float = models.DecimalField(
        verbose_name="x ->",
        decimal_places=2,
        max_digits=5,
        default=0.0,
        validators=[MaxValueValidator(100.0), MinValueValidator(0.0)],
    )
    y: float = models.DecimalField(
        verbose_name="y ↑",
        decimal_places=2,
        max_digits=5,
        default=0.0,
        validators=[MaxValueValidator(100.0), MinValueValidator(0.0)],
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        ordering = ["-image"]
        app_label = "catalog"
        db_table = "images"

    panels = [
        FieldPanel("title"),
        FieldPanel("image", widget=AdminImageChooser),
        FieldPanel("describe"),
        FieldPanel("label"),
        FieldPanel(
            "x",
            widget=forms.NumberInput(attrs={"min": 0.0, "max": 100.0}),
            classname="x",
        ),
        FieldPanel(
            "y",
            widget=forms.NumberInput(attrs={"min": 0.0, "max": 100.0}),
            classname="y",
        ),
    ]
