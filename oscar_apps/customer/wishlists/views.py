from http import HTTPStatus

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django_extensions.auth.mixins import ModelUserFieldPermissionMixin
from django_extensions.views.mixins import AdjustablePaginationMixin
from django_htmx.http import reswap, retarget
from django_tables2.paginators import LazyPaginator
from django_tables2.views import SingleTableMixin
from htmx_utils.views import HtmxActionView, HtmxModelActionView
from htmx_utils.views.mixins import HtmxFormMixin

from oscar_apps.catalogue.models import Product
from oscar_apps.wishlists.models import Line, WishList
from oscar_apps.wishlists.tables import LineTable
from oscar_apps.wishlists.utils import fetch_wishlist

from .actions import WishlistAddProductAction, WishlistRemoveProductAction


class WishListDetailView(
	AdjustablePaginationMixin, SingleTableMixin, SingleObjectMixin, TemplateView
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

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["wishlist"] = self.object
		return context


class WishListAddProduct(HtmxModelActionView):
	model = Product
	pk_url_kwarg = "product_pk"
	action_class = WishlistAddProductAction

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			self.object = self.get_object()
			return redirect(self.object)
		return redirect("index")

	def get_template_names(self):
		return ["oscar/catalogue/partials/product.html#remove-from-wishlist"]

	def get_action_kwargs(self):
		kwargs = super().get_action_kwargs()
		kwargs["product"] = self.object
		kwargs["wishlist"] = fetch_wishlist(self.request, eager=False)
		return kwargs

	def get_success_url(self):
		login_url = settings.LOGIN_URL
		if self.request.path.startswith(login_url):
			return redirect("customer:wishlist-detail")
		return self.request.path

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["product"] = self.object
		return context


class WishListUpdateLine(ModelUserFieldPermissionMixin, HtmxFormMixin, UpdateView):
	model = Line
	fields = ["quantity"]
	pk_url_kwarg = "line_pk"
	model_permission_user_field = "wishlist__owner"

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect(self.get_success_url())
		return redirect("index")

	def get_success_url(self):
		return reverse("customer:wishlist-detail")

	def form_valid(self, form):
		line = form.instance
		deleted = line.quantity <= 0

		if deleted:
			line.delete()
		else:
			line.save()

		if self.request.htmx:
			response = HttpResponse(status=HTTPStatus.NO_CONTENT)
			if deleted:
				response = reswap(retarget(response, "closest tr"), "delete")
			return response
		return redirect(self.get_success_url())


class WishListRemoveProduct(HtmxActionView):
	action_class = WishlistRemoveProductAction

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect(self.get_success_url())
		return redirect("index")

	def get_template_names(self):
		return ["oscar/catalogue/partials/product.html#add-to-wishlist"]

	def get_action_kwargs(self):
		kwargs = super().get_action_kwargs()
		kwargs["line_pk"] = self.kwargs.get("line_pk")
		kwargs["product_pk"] = self.kwargs.get("product_pk")
		kwargs["wishlist"] = fetch_wishlist(self.request, eager=False)
		return kwargs

	def get_success_url(self):
		login_url = settings.LOGIN_URL
		if self.request.path.startswith(login_url):
			return redirect("customer:wishlist-detail")
		return self.request.path

	def get_context_data(self, action, **kwargs):
		context = super().get_context_data(**kwargs)
		line, product = action.result
		context["line"] = line
		context["product"] = product
		return context
