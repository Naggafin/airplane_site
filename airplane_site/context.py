import datetime

from cachetools import TTLCache
from django.conf import settings

_cache = TTLCache(maxsize=10000, ttl=datetime.timedelta(days=1).total_seconds())


# TODO
def populate_products(request):
	return {
		"top_products": [],
		"popular_products": [],
		"recommended_products": [],
		"top_categories": [],
		"popular_categories": [],
		#'recommended_categories':[],
		"shopping_cart": [],
		"shopping_cart_total": 0.0,
		"wishlists": [],
	}
	if not request.user.is_authenticated:
		return {}
	session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
	if session_key in _cache:
		return _cache[session_key]
	_cache[session_key] = {}
	return _cache[session_key]
