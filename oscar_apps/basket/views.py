from django.contrib import messages
from django.shortcuts import get_object_or_404
from htmx_utils.views import HtmxActionView
from oscar.apps.basket.utils import BasketMessageGenerator
from oscar.apps.basket.views import (
	BasketAddView as CoreBasketAddView,
	BasketView as CoreBasketView,
)

from oscar_apps.catalogue.models import Product

from .actions import BasketRemoveAction


class BasketView(CoreBasketView):
	template_name = "pixio/shop-cart.html"


class BasketAddView(CoreBasketAddView):
	def get_template_names(self):
		if self.request.htmx:
			return ["oscar/catalogue/partials/product.html#remove-from-basket"]
		return super().get_template_names()

	def form_valid(self, form):
		offers_before = self.request.basket.applied_offers()

		self.request.basket.add_product(
			form.product, form.cleaned_data["quantity"], form.cleaned_options()
		)

		if not self.request.htmx:
			messages.success(
				self.request, self.get_success_message(form), extra_tags="safe noicon"
			)

		# Check for additional offer messages
		BasketMessageGenerator().apply_messages(self.request, offers_before)

		# Send signal for basket addition
		self.add_signal.send(
			sender=self,
			product=form.product,
			user=self.request.user,
			request=self.request,
		)

		return super().form_valid(form)


class BasketRemoveView(HtmxActionView):
	action_class = BasketRemoveAction

	def get_template_names(self, action):
		return ["oscar/catalogue/partials/product.html#add-to-basket"]

	def get_action_kwargs(self):
		kwargs = super().get_action_kwargs()
		kwargs["product"] = get_object_or_404(Product, pk=self.kwargs["pk"])
		return kwargs

	def get_success_url(self):
		return self.request.path
