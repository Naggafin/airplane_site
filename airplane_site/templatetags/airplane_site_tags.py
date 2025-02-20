from django import template
from django_tables2.paginators import LazyPaginator

register = template.Library()


@register.simple_tag
def page_range(page, paginator, page_range=10):
	"""
	Pulled from django-tables2.

	Given an page and paginator, return a list of max 10 (by default) page numbers:
	 - always containing the first, last and current page.
	 - containing one or two '...' to skip ranges between first/last and current.
	"""

	num_pages = paginator.num_pages
	if num_pages <= page_range:
		return range(1, num_pages + 1)

	range_start = page.number - int(page_range / 2)
	if range_start < 1:
		range_start = 1
	range_end = range_start + page_range
	if range_end > num_pages:
		range_start = num_pages - page_range + 1
		range_end = num_pages + 1

	ret = range(range_start, range_end)
	if 1 not in ret:
		ret = [1, "..."] + list(ret)[2:]
	if num_pages not in ret:
		ret = list(ret)[:-2] + ["...", num_pages]
	if isinstance(paginator, LazyPaginator) and not paginator.is_last_page(page.number):
		ret.append("...")
	return ret
