# core/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='dict_get')  # ← ここに 'dict_get' を明示的に指定
def dict_get(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
