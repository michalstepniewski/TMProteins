from django import template

register = template.Library()

def format83f(value): # Only one argument.
    """Converts a string into all lowercase"""
    return '%8.3f' % (value)


