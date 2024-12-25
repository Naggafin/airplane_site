from htmx_utils.view import HtmxActionView, HtmxModelActionView
from oscar.apps.customer.wishlists.views import (
	WishListAddProduct as CoreWishListAddProduct,
	WishListListView as CoreWishListListView,
)

from oscar_apps.catalogue.models import Product

from .actions import WishlistAddProductAction, WishlistRemoveProductAction


class WishListListView(CoreWishListListView):
	template_name = "pixio/shop-wishlist.html"


class WishListAddProduct(HtmxModelActionView, CoreWishListAddProduct):
	model = Product
	action_class = WishlistAddProductAction

	def get_template_names(self):
		return ["oscar/catalogue/partials/product.html#remove-from-wishlist"]

	def get_action_kwargs(self):
		kwargs = super().get_action_kwargs()
		kwargs["product"] = self.object
		kwargs["wishlist"] = self.get_or_create_wishlist(
			self.request, self.args, self.kwargs
		)
		return kwargs

	def get_success_url(self):
		return self.request.path

	def action_valid(self, action):
		# clear basket cache since it has changed
		# cache_key = BASKET_CACHE_KEY % basket.pk
		# cache.delete(cache_key)
		return super().action_valid(action)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["product"] = self.object
		context["wishlist"] = self.wishlist
		return context

	def get_or_create_wishlist(self, request, *args, **kwargs):
		wishlist = self.wishlist = super().get_or_create_wishlist(
			request, *args, **kwargs
		)
		return wishlist


class WishListRemoveProduct(HtmxActionView):
	action_class = WishlistRemoveProductAction

	def get_template_names(self):
		return ["oscar/catalogue/partials/product.html#add-to-wishlist"]

	def get_action_kwargs(self):
		kwargs = super().get_action_kwargs()
		kwargs["wishlist_key"] = (self.kwargs["key"],)
		kwargs["line_pk"] = self.kwargs.get("line_pk")
		kwargs["product_pk"] = self.kwargs.get("product_pk")
		return kwargs

	def get_success_url(self):
		return self.request.path

	def action_valid(self, action):
		# clear basket cache since it has changed
		# cache_key = BASKET_CACHE_KEY % basket.pk
		# cache.delete(cache_key)
		return super().action_valid(action)

	def get_context_data(self, action, **kwargs):
		context = super().get_context_data(**kwargs)
		product, wishlist = action.result
		context["product"] = product
		context["wishlist"] = wishlist
		return context
