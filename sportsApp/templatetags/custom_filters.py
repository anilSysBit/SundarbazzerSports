# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='custom_truncate')
def custom_truncate(value, arg):
    if len(value) > arg:
        return value[:arg] + '...'  # Customize the end string as needed
    return value