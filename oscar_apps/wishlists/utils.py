import logging

from box import Box
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Sum
from django.utils.translation import ngettext_lazy

from .constants import WISHLIST_CACHE_KEY
from .models import WishList
from .serializers import WishListSerializer

logger = logging.getLogger(__name__)

CACHE_TIMEOUT = 60 * 5  # 5 minutes


def fetch_wishlist(request):
	user = request.user
	if not user.is_authenticated:
		return None

	try:
		wishlist, created = WishList.objects.get_or_create(owner=user)
		return wishlist
	except WishList.MultipleObjectsReturned:
		logger.warning(f"Multiple wishlists found for user #{user.pk}. Merging them.")

		# Use 'prefetch_related' to ensure 'lines__product' is fetched in the merged wishlists
		wishlists = list(
			WishList.objects.filter(owner=user).annotate(
				total_lines_quantity=Sum("lines__quantity")
			)
		)

		wishlist = wishlists[0]
		num_items_merged = 0
		for other_wishlist in wishlists[1:]:
			wishlist.merge(other_wishlist)
			# NOTE: Sum can potentially return 'None', hence 'or 0'
			num_items_merged += wishlist.total_lines_quantity or 0

		if num_items_merged > 0:
			# Show warning only if items have been merged
			messages.add_message(
				request,
				messages.WARNING,
				ngettext_lazy(
					"We have merged %(num_items_merged)d item from a "
					"previous session to your wishlist.",
					"We have merged %(num_items_merged)d items from a "
					"previous session to your wishlist.",
					num_items_merged,
				)
				% {"num_items_merged": num_items_merged},
			)

		return wishlist


def get_or_create_wishlist_cache(request):
	"""
	Retrieve or create a cached wishlist for the authenticated user.

	Returns:
	    dict: Serialized wishlist data or an empty list if the user is not authenticated.
	"""

	if not request.user.is_authenticated:
		return None

	def get_cache_key(user_id):
		return WISHLIST_CACHE_KEY % user_id

	user_id = request.user.pk
	cache_key = get_cache_key(user_id)
	cached_wishlist = cache.get(cache_key)

	def box_cache(data):
		boxed = Box(data)
		boxed.lines.all = lambda: boxed.lines
		for line in boxed.lines:
			line.product_id = line.product
			line.wishlist_id = line.wishlist
		return boxed

	if cached_wishlist:
		return box_cache(cached_wishlist)

	wishlist = fetch_wishlist(request)
	if not wishlist:
		return None

	serialized_wishlist = WishListSerializer(wishlist).data
	cache.set(cache_key, serialized_wishlist, timeout=CACHE_TIMEOUT)
	return box_cache(serialized_wishlist)
