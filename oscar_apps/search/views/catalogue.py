from urllib.parse import quote

from django.contrib.auth import get_permission_codename
from django.http import Http404, HttpResponsePermanentRedirect
from django_filters.views import FilterMixin
from haystack.query import EmptySearchQuerySet
from oscar.core.loading import get_class, get_model

from oscar_apps.catalogue.filters import ProductFilter

from .base import BaseSearchView

BrowseCategoryForm = get_class("search.forms", "BrowseCategoryForm")
CategoryForm = get_class("search.forms", "CategoryForm")
Category = get_model("catalogue", "Category")


class CatalogueView(FilterMixin, BaseSearchView):
	form_class = BrowseCategoryForm
	filter_class = ProductFilter
	context_object_name = "products"
	template_name = "oscar/catalogue/browse.html"
	enforce_paths = True

	def get_category(self):
		try:
			category_pk = self.kwargs.get("pk")
			return Category.objects.get(pk=category_pk)
		except Category.DoesNotExist:
			return None

	def is_viewable(self, category, request):
		opts = category._meta
		codename = get_permission_codename("view", opts)
		has_view_perm = request.user.has_perm(
			"%s.%s" % (opts.app_label, codename), obj=category
		)
		return category.is_public or has_view_perm

	def redirect_if_necessary(self, current_path, category):
		if self.enforce_paths:
			# Categories are fetched by primary key to allow slug changes.
			# If the slug has changed, issue a redirect.
			expected_path = category.get_absolute_url()
			if expected_path != quote(current_path):
				return HttpResponsePermanentRedirect(expected_path)
		return None

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		if self.category:
			kwargs["categories"] = self.category.get_descendants_and_self()
		return kwargs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["category"] = self.category
		return context

	def get(self, request, *args, **kwargs):
		# Get the category and check if it is viewable
		self.category = self.get_category()
		if self.category:
			if not self.is_viewable(self.category, request):
				raise Http404

			# Handle potential redirect
			potential_redirect = self.redirect_if_necessary(request.path, self.category)
			if potential_redirect:
				return potential_redirect

		# Initialize the filterset and retrieve the object list
		filterset_class = self.get_filterset_class()
		self.filterset = self.get_filterset(filterset_class)

		if (
			not self.filterset.is_bound
			or self.filterset.is_valid()
			or not self.get_strict()
		):
			self.object_list = self.filterset.qs
		else:
			self.object_list = EmptySearchQuerySet()

		# Prepare the form, query, and context data
		self.form = self.get_form()
		self.query = self.get_query(self.form)
		context = self.get_context_data(
			filter=self.filterset,
			form=self.form,
			query=self.query,
			object_list=self.object_list,
		)

		# Render the response
		return self.render_to_response(context)
