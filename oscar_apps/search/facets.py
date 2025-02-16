import math

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from haystack.query import SearchQuerySet


def _create_price_range_query_facet(sqs):
	prices = [result.price for result in sqs if result.price is not None]
	if prices:
		min_price, max_price = min(prices), max(prices)
	else:
		return settings.OSCAR_SEARCH_FACETS["queries"]["price_range"]["queries"]

	min_buckets = settings.SITE_VARS["min_price_range_facets"]
	max_buckets = settings.SITE_VARS["max_price_range_facets"]
	bucket_step_size = settings.SITE_VARS["price_range_facets_bucket_step_size"]

	price_range = max_price - min_price
	num_buckets = max(
		min_buckets, min(max_buckets, math.ceil(price_range / bucket_step_size))
	)
	step = max(1, math.ceil(price_range / num_buckets))
	price_ranges = []

	for i in range(num_buckets):
		start = min_price + (i * step)
		end = start + step
		if i == num_buckets - 1:
			range_query = f"[{start} TO *]"
			label = f"{start}+"
		else:
			range_query = f"[{start} TO {end}]"
			label = _("%d to %d") % (start, end)

		price_ranges.append((label, range_query))

	return price_ranges


def base_sqs():
	sqs = SearchQuerySet()
	# make a copy of search facets so as not to modify the global copy
	search_facets = settings.OSCAR_SEARCH_FACETS.copy()
	for facet in search_facets["fields"].values():
		options = facet.get("options", {})
		sqs = sqs.facet(facet["field"], **options)
	for facet in search_facets["queries"].values():
		if facet == "price_range":
			facet["queries"] = _create_price_range_query_facet(sqs)
		for query in facet["queries"]:
			sqs = sqs.query_facet(facet["field"], query[1])

	sqs = sqs.filter_and(is_public="true", structure__in=["standalone", "parent"])
	return sqs
