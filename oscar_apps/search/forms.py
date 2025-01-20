from oscar.apps.search.forms import BrowseCategoryForm


class CategoryForm(BrowseCategoryForm):
	def __init__(self, *args, categories=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.categories = categories

	def no_query_found(self):
		"""
		Return Queryset of all the results.
		"""
		sqs = super().no_query_found()
		if not self.categories:
			return sqs

		category_ids = list(self.categories.values_list("pk", flat=True))
		return sqs.filter(category__in=category_ids)
