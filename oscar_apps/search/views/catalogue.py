from urllib.parse import quote

from django.contrib.auth import get_permission_codename
from django.http import HttpResponsePermanentRedirect
from django_extensions.views.mixins import AdjustablePaginationMixin
from django_tables2.paginators import LazyPaginator
from oscar.apps.search.views.catalogue import (
	CatalogueView as BaseCatalogueView,
	ProductCategoryView as BaseProductCategoryView,
)


class SortingMixin:
	def get_ordering(self):
		ordering = self.request.GET.getlist("sort")
		return ordering

	def get_queryset(self):
		sqs = super().get_queryset()
		ordering = self.get_ordering()
		if ordering:
			sqs = sqs.order_by(*ordering)
		return sqs


class CatalogueView(AdjustablePaginationMixin, SortingMixin, BaseCatalogueView):
	pagination_choices = [20, 30, 50, 100]
	paginator_class = LazyPaginator
	template_name = "pixio/shop.html"

	def get_template_names(self):
		if self.request.htmx:
			if self.request.htmx.target == "masonry":
				return ["oscar/catalogue/partials/browse.html"]
			return ["oscar/catalogue/partials/shop.html"]
		return super().get_template_names()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["ordering"] = self.get_ordering()
		return context


class ProductCategoryView(
	AdjustablePaginationMixin, SortingMixin, BaseProductCategoryView
):
	pagination_choices = [20, 30, 50, 100]
	paginator_class = LazyPaginator
	template_name = "pixio/shop.html"

	def get_template_names(self):
		if self.request.htmx:
			if self.request.htmx.target == "masonry":
				return ["oscar/catalogue/partials/browse.html"]
			return ["oscar/catalogue/partials/shop.html"]
		return super().get_template_names()

	def is_viewable(self, category, request):
		opts = category._meta
		codename = get_permission_codename("view", opts)
		has_view_perm = request.user.has_perm(
			"%s.%s" % (opts.app_label, codename), obj=category
		)
		return category.is_public or has_view_perm

	def redirect_if_necessary(self, current_path, category):
		if self.enforce_paths and not self.request.htmx:
			expected_path = category.get_absolute_url()
			if expected_path != quote(current_path):
				return HttpResponsePermanentRedirect(expected_path)
		return None

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["ordering"] = self.get_ordering()
		return context
