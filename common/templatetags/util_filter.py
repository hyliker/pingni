#coding: utf-8
from django.template import Library

register = Library()

@register.filter
def charwrap(value, num=None):
    import textwrap
    if num is None:
        return value
    else:
        return "\n".join(textwrap.wrap(value, num))
