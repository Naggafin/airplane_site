from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django_extensions.views.mixins import AdjustablePaginationMixin
from django_tables2.paginators import LazyPaginator
from django_tables2.views import SingleTableMixin
from htmx_utils.views import HtmxActionView, HtmxModelActionView
from htmx_utils.views.mixins import HtmxFormMixin
from view_breadcrumbs import DetailBreadcrumbMixin

from oscar_apps.catalogue.models import Product
from oscar_apps.wishlists.models import Line, WishList
from oscar_apps.wishlists.tables import LineTable

from .actions import WishlistAddProductAction, WishlistRemoveProductAction


class WishListDetailView(
	AdjustablePaginationMixin,
	SingleTableMixin,
	SingleObjectMixin,
	DetailBreadcrumbMixin,
	TemplateView,
):
	model = WishList
	slug_field = "key"
	table_class = LineTable
	paginator_class = LazyPaginator
	template_name = "pixio/shop-wishlist.html"

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object_list = self.get_object_list()
		context = self.get_context_data(
			object=self.object, object_list=self.object_list
		)
		return self.render_to_response(context)

	def get_queryset(self):
		return self.model.prefetch_related(
			"lines__product__stockrecords", "lines__product__images"
		).all()

	def get_object(self, queryset=None):
		try:
			obj = super().get_object(queryset=queryset)
			if not obj.is_allowed_to_see(self.request.user):
				raise Http404
			return obj
		except AttributeError:
			if not self.request.user.is_authenticated:
				return redirect("pixio:index")
			return self.request.wishlist
		except Http404:
			if not self.request.user.is_authenticated:
				raise
			return redirect("customer:wishlist-detail")

	def get_object_list(self):
		return self.object.lines.all()

	def get_table_kwargs(self):
		kwargs = super().get_table_kwargs()
		if not self.object.is_allowed_to_edit(self.request.user):
			if "exclude" not in kwargs:
				kwargs["exclude"] = []
			kwargs["exclude"] = list(kwargs["exclude"]) + ["line_add", "line_remove"]
		return kwargs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["wishlist"] = self.object
		return context

	@property
	def crumbs(self):
		return [(self.detail_view_label, self.detail_view_url)]


class WishListAddProduct(LoginRequiredMixin, HtmxModelActionView):
	model = Product
	pk_url_kwarg = "product_pk"
	action_class = WishlistAddProductAction

	def get(self, request, *args, **kwargs):
		return redirect(self.get_success_url())

	def get_template_names(self):
		return ["oscar/wishlist/partials/wishlist_line_add_partial.html"]

	def get_action_kwargs(self):
		kwargs = super().get_action_kwargs()
		kwargs["product"] = self.object
		kwargs["wishlist"] = self.request.wishlist
		return kwargs

	def get_success_url(self):
		return reverse("customer:wishlist-detail")

	def get_context_data(self, action, **kwargs):
		context = super().get_context_data(**kwargs)
		line, product = action.result
		context["line"] = line
		context["product"] = product
		return context


class WishListUpdateLine(LoginRequiredMixin, HtmxFormMixin, UpdateView):
	model = Line
	fields = ["quantity"]
	pk_url_kwarg = "line_pk"

	def get(self, request, *args, **kwargs):
		return redirect(self.get_success_url())

	def get_queryset(self):
		return self.request.wishlist.lines.all()

	def get_success_url(self):
		return reverse("customer:wishlist-detail")

	def form_valid(self, form):
		line = form.instance
		product = line.product
		deleted = line.quantity <= 0

		if deleted:
			line.delete()
		else:
			line.save()

		if self.request.htmx:
			context = {
				"line": line,
				"product": product,
			}
			template = (
				"oscar/wishlist/partials/wishlist_line_remove_partial.html"
				if deleted
				else "oscar/wishlist/partials/wishlist_line_update_partial.html"
			)
			return render(self.request, template, context)
		return redirect(self.get_success_url())


class WishListRemoveProduct(LoginRequiredMixin, HtmxActionView):
	action_class = WishlistRemoveProductAction

	def get(self, request, *args, **kwargs):
		return redirect(self.get_success_url())

	def get_template_names(self):
		return ["oscar/wishlist/partials/wishlist_line_remove_partial.html"]

	def get_action_kwargs(self):
		kwargs = super().get_action_kwargs()
		kwargs["line_pk"] = self.kwargs.get("line_pk")
		kwargs["product_pk"] = self.kwargs.get("product_pk")
		kwargs["wishlist"] = self.request.wishlist
		return kwargs

	def get_success_url(self):
		return reverse("customer:wishlist-detail")

	def get_context_data(self, action, **kwargs):
		context = super().get_context_data(**kwargs)
		line, product = action.result
		context["line"] = line
		context["product"] = product
		return context
