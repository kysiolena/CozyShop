from django import template

register = template.Library()


@register.filter
def sale_price(value: int | float, sale: int | float) -> float:
    """
    Get sale price of the product by value's sale in percentage and full product price.

    :param value:
    :param sale:
    :return:
    """
    if sale:
        return round(value - (value * sale), 2)

    return value
