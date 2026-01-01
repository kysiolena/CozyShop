from django import template

register = template.Library()


@register.filter
def times(end: int, start: int = 0):
    return range(start, end + start)
