from django import template
import bleach

register = template.Library()

@register.filter

def bleach_clean(value):
    cleaned_value = bleach.clean(value, tags=[], attributes={}, strip=True)
    return cleaned_value