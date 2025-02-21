from collections import defaultdict

from oscar.apps.search.views.base import BaseSearchView as CoreBaseSearchView


class BaseSearchView(CoreBaseSearchView):
	load_all = False
	optimize_results = True

	def get_optimized_queryset(self, model, pks):
		raise NotImplementedError

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.optimize_results:
			results = context["object_list"]
			result_pks = defaultdict(list)
			for result in results:
				result_pks[result.model].append(result.pk)
			optimized_querysets = []
			for Model in result_pks:
				optimized_querysets.append(
					self.get_optimized_queryset(Model, result_pks[Model])
				)
			optimized_results = {}
			for queryset in optimized_querysets:
				optimized_results[queryset.model] = {}
				for obj in queryset:
					optimized_results[queryset.model][str(obj.pk)] = obj
			for result in results:
				result.object = optimized_results[result.model][result.pk]
		return context
