import os

from persons.apps import DEBUG
from project import BASE_DIR

# ============================================
# WEBPACK_LOADER
# ============================================
WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "static",
        "STATS_FILE": os.path.join(BASE_DIR, "bundles/webpack-stats.json"),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        "TEST": {
            "NAME": "test_cloud",
        },
        "IGNORE": [
            # '.+\.map$'
            r".+\.hot-update.js",
            r".+\.map",
        ],
        "LOADER_CLASS": "webpack_loader.loader.WebpackLoader",
    }
}


# ============================================
# SWAGGER
# ============================================
# https://drf-yasg.readthedocs.io/en/stable/security.html#security-definitions

SWAGGER_USE_COMPAT_RENDERERS = False
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "USE_SESSION_AUTH": False,
    "JSON_EDITOR": True,
    "VALIDATOR_URL": None,
    "exclude_namespaces": [],
}
SPECTACULAR_SETTINGS = {
    "TITLE": "Your API",
    "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
# ============================================
# BOOTSTRAP4
# ============================================
BOOTSTRAP4 = {
    "css_url": {
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css",
        "integrity": "sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn",
        "crossorigin": "anonymous",
    },
    # The complete URL to the Bootstrap bundle JavaScript file.
    "javascript_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-fQybjgWLrvvRgtW6bFlB7jaZrFsaBXjsOMm/tB9LTS58ONXgqbR9W8oWht/amnpF",
        "crossorigin": "anonymous",
    },
}
