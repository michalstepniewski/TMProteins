from django import template

register = template.Library()

@register.filter(name='format83f')
def format83f(value): # Only one argument.
    """Converts a string into all lowercase"""
    return '%8.3f' % (value)


