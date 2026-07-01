
## Add
```text
# project/settings_conf/settings_first.py

# ...
# ============================================
# APPLICATION DEFINITION
# ============================================
INSTALLED_APPS = [
    # ...
    "wagtail.documents", 
    # ...
    "download",
]

# ...

TEMPLATES["DIRS"] = [
            # ...
            os.path.join(BASE_DIR, "download/templates"),
        ]
# ...
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATICFILES_DIRS = [
    # ...
    os.path.join(BASE_DIR / "download/static"),
]
```
