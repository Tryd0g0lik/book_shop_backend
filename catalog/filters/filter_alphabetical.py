# catalog/filters/filter_alphabetical.py:1
import re

from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _

LIST_CHAR = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "Э",
    "Б",
    "В",
    "Г",
    "Д",
    "Е",
    "Ё",
    "Ж",
    "З",
    "И",
    "Й",
    "К",
    "Л",
    "М",
    "Н",
    "О",
    "П",
    "Р",
    "С",
    "Т",
    "У",
    "Ф",
    "Х",
    "Ц",
    "Ч",
    "Ш",
    "Щ",
    "Ъ",
    "Ы",
    "Ь",
    "Э",
    "Ю",
    "Я",
]


class AlphabeticalFilter(SimpleListFilter):
    title = _("Name (A-Z & А-Я)")
    parameter_name = "product_name"

    def lookups(self, request, model_admin):
        return [(letter, letter) for letter in LIST_CHAR]

    def queryset(self, request, queryset):
        selected = self.value()
        if not selected:
            return queryset
        if not re.match(r"[A-ZА-ЯЪ]$", selected):
            return queryset
        return queryset.filter(name__istartswith=selected)
