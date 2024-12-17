import datetime
import random

from cachetools import TTLCache
from django.conf import settings

from oscar_apps.catalogue.models import Category, Product

_cache = TTLCache(maxsize=10000, ttl=datetime.timedelta(days=1).total_seconds())


# TODO
def populate_products(request):
	products = list(
		Product.objects.all()
		.select_related("parent", "product_class")
		.prefetch_related("images", "stockrecords")
	)
	categories = list(Category.objects.all())
	return {
		"top_products": random.sample(products, 5),
		"popular_products": random.sample(products, 20),
		"recommended_products": random.sample(products, 10),
		"top_categories": random.sample(categories, 5),
		"popular_categories": random.sample(categories, len(categories)),
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
