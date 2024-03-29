from django import template

register = template.Library()


@register.simple_tag
def purchase_info_for_product(request, product):
    if product.is_parent:
        return request.strategy.fetch_for_parent(product)

    return request.strategy.fetch_for_product(product)


@register.simple_tag
def purchase_info_for_line(request, line):
    return request.strategy.fetch_for_line(line)


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def percent(value, arg):
    return value * (1-arg/100)