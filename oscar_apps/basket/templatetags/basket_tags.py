from oscar.templatetags import basket_tags

from ..utils import get_or_create_basket_cache

register = basket_tags.register


@register.filter
def is_in_basket(product, request):
	"""
	Template filter to check if a product is in the user's basket.
	"""
	if not request.user.is_authenticated:
		return False

	cached_basket = get_or_create_basket_cache(request)
	product_pks = set(line.product for line in cached_basket.lines)

	return product.pk in product_pks
