from urllib.parse import quote

from django.contrib.auth import get_permission_codename
from django.http import HttpResponsePermanentRedirect
from django_extensions.views.mixins import AdjustablePaginationMixin
from oscar.apps.search.views.catalogue import (
	CatalogueView as BaseCatalogueView,
	ProductCategoryView as BaseProductCategoryView,
)


class CatalogueView(AdjustablePaginationMixin, BaseCatalogueView):
	pagination_choices = [20, 30, 50, 100]
	template_name = "pixio/shop.html"

	def get_template_names(self):
		if self.request.htmx:
			return ["oscar/catalogue/partials/browse.html"]
		return super().get_template_names()


class ProductCategoryView(AdjustablePaginationMixin, BaseProductCategoryView):
	pagination_choices = [20, 30, 50, 100]
	template_name = "pixio/shop.html"

	def get_template_names(self):
		if self.request.htmx:
			return ["oscar/catalogue/partials/browse.html"]
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
