# cart/models/models_card.py:1
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

refer_regex = r"(media\/[a-zA-Z0-9_\-\/]+/)$"


class OrderItemModel(models.Model):
    # product = models.ForeignKey(
    #     to="catalog.ProductModel",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     verbose_name=_("Product"),
    #     limit_choices_to={"is_active": True},
    # )
    description = models.CharField(
        max_length=100,
    )
    image = models.CharField(validators=[RegexValidator(regex=refer_regex)])
    index_product = models.OneToOneField(
        to="catalog.ProductModel", on_delete=models.SET_NULL, null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=0)
    cost = models.PositiveIntegerField(default=0)  # 1 shtuka
    is_paid = models.BooleanField(default=False)  # True значит был проплачен

    def __str__(self):
        return f"{self.index_product} cost {self.cost}"

    class Meta:
        db_table = "cart"
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
        ordering = ["-quantity", "-cost"]
        indexes = [
            models.Index(fields=["index_product", "cost", "is_paid"]),
        ]
        unique_together = ("index_product",)


class CartOrderModel(models.Model):
    pass


class CartModel(models.Model):
    # cart_owner = models.ForeignKey(to=,)
    pass
