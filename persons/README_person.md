|**role**| **is_superuser**| **is_staff**||
|:---|:----------------|:------------|:---|
|*Sup-Admin*| *True*          | *True*      ||
|*Moderator*| *False*        | *True*      ||
|*Manager*| *False*        | *True*     ||
|*Editor*| *False*         | *True*      ||
|*Clients*| *False*         | *False*     ||
||                 |             ||


## The Email settings


```.env
APP_EMAIL_HOST=smtp.mail.ru
APP_EMAIL_PORT=465
# # https://docs.djangoproject.com/en/6.0/ref/settings/#default-from-email
APP_DEFAULT_FROM_EMAIL=< your_email >
APP_EMAIL_HOST_PASSWORD=< password_for_external_app_from_the_mailru_server >
```

```text

# Email configuration for the mail.ru
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USE_TLS=True
EMAIL_HOST_USER = APP_DEFAULT_FROM_EMAIL
SERVER_EMAIL = APP_DEFAULT_FROM_EMAIL
DEFAULT_FROM_EMAIL = APP_DEFAULT_FROM_EMAIL
DEFAULT_FROM_EMAIL=your-email@gmail.com
CONTACT_EMAIL=recipient@example.com

EMAIL_USE_TLS = False
EMAIL_USE_SSL = True


MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "OPTIONS": {
            "host": f"{(lambda:  EMAIL_HOST)()}",
            "use_tls": EMAIL_USE_TLS,
            "username": f"{(lambda:  APP_DEFAULT_FROM_EMAIL)()}",
            "password": f"{(lambda:  EMAIL_HOST_PASSWORD)()}",
        },
    },
}
``` 

