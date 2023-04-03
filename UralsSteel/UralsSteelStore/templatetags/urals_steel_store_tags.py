from django import template
from django.db.models import Count

from UralsSteelStore.models import *

register = template.Library()

@register.inclusion_tag('UralsSteelStore/index_category_list.html')
def show_index_category_list(category_id):
    all_categories = Category_mp.objects.annotate(cnt=Count('products')).filter(cnt__gt=0)
    products = Products.objects.filter(category=category_id)
    naw_cat = Category_mp.objects.get(pk=category_id)

    return {'all_categories': all_categories, 'products': products, 'naw_cat': naw_cat}