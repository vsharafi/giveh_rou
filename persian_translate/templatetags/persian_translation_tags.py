from django import template
from store.models import Color

register = template.Library()

@register.filter
def trans_number(value):
    value = str(value)
    e_to_p_table = value.maketrans('1234567890', '۱۲۳۴۵۶۷۸۹۰')
    return value.translate(e_to_p_table)


@register.filter
def trans_color(value):
    value = Color.objects.filter(name = value)[0]
    
    return value.farsi_name
