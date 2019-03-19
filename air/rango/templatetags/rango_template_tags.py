from django import template
from rango.models import Category

register = template.Library()


@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(), 'act_cat': cat}
	
@register.simple_tag(takes_context=True)
def is_not_homepage(context):
    if context.request.path != "/":
        return True
    else:
        return False