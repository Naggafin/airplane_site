from oscar.templatetags import wishlist_tags

from ..utils import get_or_create_wishlist_cache

register = wishlist_tags.register


@register.filter
def is_in_wishlists(product, request):
	"""
	Template filter to check if a product is in the user's wishlists.
	"""
	if not request.user.is_authenticated:
		return False

	cached_wishlist = get_or_create_wishlist_cache(request)
	product_pks = set(line.product for line in cached_wishlist.lines)

	return product.pk in product_pks
