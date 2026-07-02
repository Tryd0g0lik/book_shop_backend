# catalog/filters/filter_prices.py:1
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from catalog.filters import AlphabeticalFilter


class PriceFilter(AlphabeticalFilter):
    title = _("Price")

    parameter_name = "prices"

    def lookups(self, request, model_admin):

        return [
            ("high_to_low", format_html('<i class="bi bi-arrow-bar-down">{}</i>', "")),
            ("low_to_high", format_html('<i class="bi bi-arrow-bar-up">{}</i>', "")),
        ]

    def queryset(self, request, queryset):
        selected = self.value()
        if not selected:
            return queryset
        elif selected == "high_to_low":
            return queryset.order_by("-price")
        return queryset.order_by("price")
