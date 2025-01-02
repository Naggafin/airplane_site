from django.conf import settings
from django.http import Http404, reverse
from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
from django_extensions.auth.mixins import ModelUserFieldPermissionMixin
from django_htmx.http import reswap, retarget
from htmx_utils.views import HtmxActionView, HtmxModelActionView
from htmx_utils.views.mixins import HtmxFormMixin

from oscar_apps.catalogue.models import Product
from oscar_apps.wishlists.models import Line, WishList

from .actions import WishlistAddProductAction, WishlistRemoveProductAction
from .utils import fetch_wishlist


class WishListDetailView(DetailView):
	model = WishList
	slug_field = "key"
	template_name = "pixio/shop-wishlist.html"

	def get_queryset(self):
		queryset = super().get_queryset().prefetch_related("lines__product")
		return queryset

	def get_object(self, queryset=None):
		try:
			obj = super().get_object(queryset=queryset)
			if not obj.is_allowed_to_see(self.request.user):
				raise Http404
		except Http404:
			if not self.request.is_authenticated:
				raise
			return redirect("customer:wishlist-detail")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["wishlist"] = self.object
		return context


class WishListAddProduct(HtmxModelActionView):
	model = Product
	pk_url_kwarg = "product_pk"
	action_class = WishlistAddProductAction

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
		if request.is_authenticated:
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
			response = str(form)
			if deleted:
				response = reswap(retarget(response, "closest tr"), "delete")
			return response

		return redirect(self.get_success_url())


class WishListRemoveProduct(HtmxActionView):
	action_class = WishlistRemoveProductAction

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
