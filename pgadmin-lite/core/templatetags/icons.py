from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def icon(name, extra_classes='', title=''):
    if name == "edit":
        classes = f"fa-solid fa-pencil {extra_classes}".strip()
        title_attr = f' title="{title}"' if title else ''
        return mark_safe(f'<i class="{classes}"{title_attr}></i>')
    return ''