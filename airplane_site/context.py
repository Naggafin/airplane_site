import datetime
import random

from cachetools import TTLCache, cached
from django.conf import settings
from oscar.core.loading import get_model

Category = get_model("catalogue", "Category")
Product = get_model("catalogue", "Product")
ProductClass = get_model("catalogue", "ProductClass")

_cache = TTLCache(maxsize=1000, ttl=datetime.timedelta(days=1).total_seconds())


def site_ui(request):
	return settings.SITE_UI_VARS


def _get_cache_key(request):
	return request.COOKIES.get(settings.SESSION_COOKIE_NAME)


# TODO 1: implement real logic to populate these lists
@cached(cache=_cache, key=_get_cache_key)
def populate_products(request):
	products = list(Product.objects.base_queryset().all())
	product_classes = list(ProductClass.objects.all())
	categories = list(Category.objects.filter(depth=1))
	context = {
		"top_products": random.sample(
			products, settings.SITE_UI_VARS["num_top_products"]
		),
		"popular_products": random.sample(
			products, settings.SITE_UI_VARS["num_popular_products"]
		),
		"recommended_products": random.sample(
			products, settings.SITE_UI_VARS["num_recommended_products"]
		),
		"top_product_classes": random.sample(
			product_classes,
			min(len(product_classes), settings.SITE_UI_VARS["num_top_product_classes"]),
		),
		"popular_product_classes": random.sample(
			product_classes,
			min(
				len(product_classes),
				settings.SITE_UI_VARS["num_popular_product_classes"],
			),
		),
		"top_categories": random.sample(
			categories,
			min(len(categories), settings.SITE_UI_VARS["num_top_categories"]),
		),
		"popular_categories": random.sample(
			categories,
			min(len(categories), settings.SITE_UI_VARS["num_popular_categories"]),
		),
	}
	return context
