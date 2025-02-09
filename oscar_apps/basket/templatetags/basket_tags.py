from oscar.templatetags import basket_tags

from ..utils import get_or_create_basket_cache

register = basket_tags.register


@register.filter
def is_in_basket(product, request):
	cached_basket = get_or_create_basket_cache(request)
	product_pks = set(line.product_id for line in cached_basket.lines.all())
	return product.pk in product_pks


@register.simple_tag
def product_quantity_in_basket(request, product):
	cached_basket = get_or_create_basket_cache(request)
	product_pks = [line.product_id for line in cached_basket.lines.all()]
	return product_pks.count(product.pk)
