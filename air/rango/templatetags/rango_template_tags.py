from django import template
from rango.models import *

register = template.Library()



@register.simple_tag(takes_context=True)
def is_not_homepage(context):
    if context.request.path != "/":
        return True
    else:
        return False
