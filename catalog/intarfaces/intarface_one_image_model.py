from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from django.db import models
    from modelcluster.fields import ParentalKey
    from wagtail.admin.panels import FieldPanel


class OneImageModelsType(Protocol):
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
    title: str
    image: models.ForeignKey
    product: ParentalKey
    describe: str
    label: str
    x: float
    y: float

    models = None

    def __str__(self) -> str: ...

    panels: list[FieldPanel]
