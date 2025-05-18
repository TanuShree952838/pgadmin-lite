from django import template

register = template.Library()

@register.filter
def get_item(obj, key):
    # Try dict-like access
    if isinstance(obj, dict):
        return obj.get(key, '')
    # Try tuple/list index access
    try:
        return obj[key]
    except (IndexError, KeyError, TypeError):
        return ''

      
@register.filter
def get_index(lst, idx):
    try:
        return lst[idx]
    except (IndexError, TypeError):
        return ''


@register.filter
def make_range(n):
    return range(n)
