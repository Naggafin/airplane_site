import auto_prefetch
from django.db.models import Prefetch
from oscar.apps.catalogue.managers import (
	CategoryQuerySet as CoreCategoryQuerySet,
	ProductQuerySet as CoreProductQuerySet,
)


class ProductQuerySet(auto_prefetch.QuerySet, CoreProductQuerySet):
	def prefetch_public_children(self, queryset=None):
		if queryset is None:
			queryset = self.model.objects.public().prefetch_related("stockrecords")

		return self.prefetch_related(
			Prefetch(
				"children",
				queryset=queryset,
				to_attr="_prefetched_public_children",
			)
		)


class CategoryQuerySet(auto_prefetch.QuerySet, CoreCategoryQuerySet):
	pass
