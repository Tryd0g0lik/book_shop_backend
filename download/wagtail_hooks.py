# download/wagtail_hooks.py:1
# catalog/wagtail_hooks.py:1
import json
import os
import re
from os import path

from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from wagtail import hooks

from project import BASE_DIR


@hooks.register("insert_global_admin_js")
def insert_catalog_js():
    try:
        # Create a parent a file for start a js code.

        path_str: str = str(
            path.join(BASE_DIR / "download/static/scripts/wagtail-admin")
        )
        # Get a path to the js files
        if os.access(path_str, os.R_OK):
            # Write a new content for a amin js file
            list_dir: list = os.listdir(path=path_str)
            str_body: str = ""
            for fn in list_dir:
                # New content: Connection a new logic of interface for the Wagtail damin
                str_0: str = 'import "{}"; \n\t'
                if re.match(r"[\w-]+\.js$", fn, re.IGNORECASE):
                    str_0 = str_0.format(
                        ".\\" + path_str.split("static\\scripts\\")[-1] + "\\" + fn
                    )
                    str_0 = str_0.replace("\\", "/")
                    str_body += str_0
            # Create the main js file
            script_url = static("scripts/download_wagtail_admins.js")
            with open(
                path_str.replace("wagtail-admin", "") + script_url.split("/")[-1], "w"
            ) as f:
                f.write(str_body)
            # Send data to the html template of the Wagtail admin.
            # Connection the new js logic.
            return format_html(
                """
            <script type="module" src="{}"></script>
            </script>
            """,
                script_url,
            )

        return None
    except Exception as e:
        print(e)
