#coding: utf-8
#http://gnuvince.wordpress.com/2007/09/14/a-django-template-tag-for-the-current-active-page/
import re
from django.template import Library
from django.core.urlresolvers import reverse

register = Library()

@register.simple_tag
def navactive(request, pattern, return_value="active"):
    if re.search(pattern, request.path):
        return return_value
    return ""

@register.simple_tag
def reverse_navactive(request, url, return_value="active"):
    if reverse(url) == request.path:
        return return_value
    return ""
