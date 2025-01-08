import datetime
import random

from cachetools import TTLCache
from django.conf import settings

from oscar_apps.catalogue.models import Category, Product

_cache = TTLCache(maxsize=10000, ttl=datetime.timedelta(days=1).total_seconds())


def site_ui(request):
	return settings.SITE_UI_VARS


# TODO 1: implememt real logic to populate these lists
# TODO 2: implement caching for performance
def populate_products(request):
	session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
	if session_key in _cache:
		return _cache[session_key]
	products = list(
		Product.objects.select_related("parent", "product_class")
		.prefetch_related("images", "stockrecords")
		.all()
	)
	categories = list(Category.objects.all())
	_cache[session_key] = context = {
		"top_products": random.sample(products, 5),
		"popular_products": random.sample(products, 20),
		"recommended_products": random.sample(products, 10),
		"top_categories": random.sample(categories, 5),
		"popular_categories": random.sample(categories, len(categories)),
		#'recommended_categories':[],
	}
	return context
