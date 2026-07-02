
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

- '`download/templates/modeladmin/includes/header.html`'\
HTML Template of button for a page where we can see full list of the database's positions.  \
- '`download/static/modal_pages/confirm_convert_alias.txt`'\
HML template a form. This form we can see when want to load file to the server and add position in catalog '`template_catalog.xls`'  

[![img](/img/file_xsl_small.png)](/img/file_xsl_large.png)

**You can use files from the '`*.xls`' or `*.xlsx`' & strictly presented a template**. 


- Wne you sent your file in the form data, first file will be load to temporary storage. Tha is  '`media/temp/chunked_uploads`' through chucks.
- Then it''ll will be converted to the full format by path '`media/documents`'.
- After begin a process saving to database.  
**Note:** Data that has not been saved in database will be saving in path "`media/error_catalog/product_error_01-07-20 ..*.. 2.txt`".\
    Every file can to have a size 800 KB and size a low than it.
