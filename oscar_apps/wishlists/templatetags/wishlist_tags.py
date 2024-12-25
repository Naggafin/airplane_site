from django.core.cache import cache
from oscar.apps.wishlists.models import WishList
from oscar.templatetags import wishlist_tags

from ..constants import WISHLIST_CACHE_KEY

CACHE_TIMEOUT = 60 * 5  # 5 minutes

register = wishlist_tags.register


@register.filter
def is_in_wishlists(product, request):
	"""
	Optimized template filter to check if a product is in the user's wishlists.
	Caches the wishlists' product IDs to reduce database queries.
	"""
	if not request.user.is_authenticated:
		return False

	user_id = request.user.pk
	cache_key = WISHLIST_CACHE_KEY % user_id
	product_ids = cache.get(cache_key)

	if product_ids is None:
		product_ids = set(
			WishList.objects.filter(owner=user_id).values_list(
				"lines__product_id", flat=True
			)
		)
		cache.set(cache_key, product_ids, timeout=CACHE_TIMEOUT)

	return product.id in product_ids
