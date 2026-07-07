# persons/templatetags/user_display_db.py:1
from django import template

register = template.Library()


@register.filter
def user_display(user):
    if user:
        return user.email
    return ""
