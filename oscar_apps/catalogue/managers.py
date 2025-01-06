import auto_prefetch
from oscar.apps.catalogue.managers import (
	CategoryQuerySet as CoreCategoryQuerySet,
	ProductQuerySet as CoreProductQuerySet,
)


class ProductQuerySet(auto_prefetch.QuerySet, CoreProductQuerySet):
	pass


class CategoryQuerySet(auto_prefetch.QuerySet, CoreCategoryQuerySet):
	pass
