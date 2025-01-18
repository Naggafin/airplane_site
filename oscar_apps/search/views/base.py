from django.conf import settings
from django.views.generic.base import ContextMixin, TemplateResponseMixin, View
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from haystack.constants import RESULTS_PER_PAGE
from haystack.forms import FacetedSearchForm, ModelSearchForm
from oscar.core.loading import get_class

FacetMunger = get_class("search.facets", "FacetMunger")
base_sqs = get_class("search.facets", "base_sqs")


class SearchView(
	TemplateResponseMixin, FormMixin, MultipleObjectMixin, ContextMixin, View
):
	template_name = "search/search.html"
	form_class = ModelSearchForm
	searchqueryset = None
	load_all = True
	results_per_page = RESULTS_PER_PAGE

	def get_form_kwargs(self):
		"""
		Extends the form kwargs to include `searchqueryset` and `load_all`.
		"""
		kwargs = super().get_form_kwargs()
		kwargs.update(
			{
				"searchqueryset": self.searchqueryset,
				"load_all": self.load_all,
			}
		)
		return kwargs

	def get_query(self, form):
		"""
		Extracts the query from the form.
		"""
		return form.cleaned_data["q"] if form.is_valid() else ""

	def get_queryset(self, form=None):
		"""
		Executes the search and returns the results.
		"""
		if not hasattr(self, "_queryset"):
			form = form or self.form
			self._queryset = form.search()
		return self._queryset

	def get_context_data(self, **kwargs):
		"""
		Constructs the context for rendering the template.
		"""
		form = kwargs.pop("form", self.form)
		query = kwargs.pop("query", self.query)
		queryset = kwargs.pop("object_list", self.object_list)

		context = {
			"form": form,
			"query": query,
			"object_list": queryset,
			"suggestion": None,
			**kwargs,
		}

		if hasattr(queryset, "query") and queryset.query.backend.include_spelling:
			context["suggestion"] = form.get_suggestion()

		return super().get_context_data(**context)

	def get(self, request, *args, **kwargs):
		"""
		Handles GET requests.
		"""
		self.form = self.get_form()
		self.query = self.get_query(self.form)
		self.object_list = self.get_queryset(self.form)
		context = self.get_context_data(
			form=self.form, query=self.query, object_list=self.object_list
		)
		return self.render_to_response(context)


class BaseFacetedSearchView(SearchView):
	form_class = FacetedSearchForm

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs["selected_facets"] = self.request.GET.getlist("selected_facets")
		return kwargs

	def get_context_data(self, **kwargs):
		context = {"facets": self.object_list.facet_counts(), **kwargs}
		return super().get_context_data(**context)


class BaseSearchView(BaseFacetedSearchView):
	facet_fields = settings.OSCAR_SEARCH_FACETS["fields"].keys()
	paginate_by = settings.OSCAR_PRODUCTS_PER_PAGE

	def get_queryset(self, form=None):
		if not hasattr(self, "_queryset"):
			self._queryset = base_sqs()
		return self._queryset

	def get_context_data(self, form=None, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)

		form = form if form is not None else self.form
		queryset = object_list if object_list is not None else self.object_list

		# Convert facet data into a more useful data structure
		if "fields" in context["facets"]:
			munger = FacetMunger(
				self.request.get_full_path(),
				form.selected_multi_facets,
				queryset.facet_counts(),
				query_type=type(queryset.query),
			)
			context["facet_data"] = munger.facet_data()
			context["has_facets"] = any(
				[len(data["results"]) for data in context["facet_data"].values()]
			)

		context["selected_facets"] = form.selected_facets

		return context
