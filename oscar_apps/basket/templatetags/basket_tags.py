from django.core.cache import cache
from oscar.templatetags import basket_tags

from ..constants import BASKET_CACHE_KEY

register = basket_tags.register


@register.filter(needs_context=True)
def is_in_basket(product, request):
	"""
	Optimized template filter to check if a product is in the user's basket.
	Caches the basket's product IDs to reduce database queries.
	"""
	basket = getattr(request, "basket", None)
	if not basket:
		return False  # If the basket is not available, return False

	# Cache key based on the user's basket ID
	cache_key = BASKET_CACHE_KEY % basket.pk
	product_ids = cache.get(cache_key)

	if product_ids is None:
		# Cache miss: Fetch product IDs from the basket lines and cache them
		product_ids = set(basket.lines.values_list("product_id", flat=True))
		cache.set(cache_key, product_ids, timeout=300)  # Cache for 5 minutes

	# Check if the product ID is in the cached product IDs
	return product.pk in product_ids
