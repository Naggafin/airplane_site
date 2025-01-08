import logging

from box import Box
from django.core.cache import cache
from oscar.apps.basket.utils import *  # noqa: F403

from .constants import BASKET_CACHE_KEY

logger = logging.getLogger(__name__)

CACHE_TIMEOUT = 60 * 5  # 5 minutes


def get_or_create_basket_cache(request):
	"""
	Retrieve or create a cached basket for the given request.

	Returns:
	    dict: Serialized basket data or an empty list if no basket exists.
	"""
	from oscar.apps.basket.middleware import BasketMiddleware

	from .serializers import BasketSerializer

	middleware = BasketMiddleware(None)

	def get_cache_key():
		if request.user.is_authenticated:
			return BASKET_CACHE_KEY % request.user.pk
		cookie_key = middleware.get_cookie_key(request)
		return BASKET_CACHE_KEY % request.COOKIES.get(cookie_key, "")

	cache_key = get_cache_key()
	cached_basket = cache.get(cache_key)

	def box_cache(data):
		boxed = Box(data)
		boxed.lines.all = lambda: boxed.lines
		for line in boxed.lines:
			line.product_id = line.product
			line.basket_id = line.basket
		return boxed

	if cached_basket:
		return box_cache(cached_basket)

	basket = middleware.get_basket(request)
	if not basket:
		return []

	serialized_basket = BasketSerializer(basket).data
	cache.set(cache_key, serialized_basket, timeout=CACHE_TIMEOUT)
	return box_cache(serialized_basket)
