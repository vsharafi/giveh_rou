from django import template

register = template.Library()


@register.simple_tag
def my_url(value, field_name, urlencode=None):
    url = f'?{field_name}={value}'

    if urlencode:
        querystrig = urlencode.split('&')
        filter_querystrig = filter(lambda p: p.split('=')[0]!=field_name, querystrig)
        encode_querystring = '&'.join(filter_querystrig)
        url = f'{url}&{encode_querystring}'

    return url