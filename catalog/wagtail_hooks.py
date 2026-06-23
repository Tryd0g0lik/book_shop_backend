# catalog/wagtail_hooks.py:1
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from wagtail import hooks


@hooks.register("insert_global_admin_js")
def insert_catalog_js():
    script_url = static("scripts/wagtail_admins.js")
    return format_html(
        """
    <script type="module" src="{}"></script>
    </script>
    """,
        script_url,
    )
