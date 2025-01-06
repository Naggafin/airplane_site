from http import HTTPStatus

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_htmx.http import trigger_client_event
from htmx_utils.views import HtmxModelActionView
from oscar.apps.basket.utils import BasketMessageGenerator
from oscar.apps.basket.views import (
	BasketAddView as CoreBasketAddView,
	BasketView as CoreBasketView,
)

from airplane_site.utils import render_table_row
from oscar_apps.catalogue.models import Product
from oscar_apps.wishlists.tables import LineTable

from .actions import BasketRemoveAction


class BasketView(CoreBasketView):
	template_name = "pixio/shop-cart.html"


class BasketAddView(CoreBasketAddView):
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

		if self.request.htmx:
			if self.request.htmx.current_url_abs_path.startswith(
				reverse("customer:wishlist-detail")
			):
				line = get_object_or_404(
					self.request.wishlist.lines.all(), product_id=form.product.pk
				)
				return render_table_row(self.request, LineTable, line)
			else:
				return render(
					self.request,
					"oscar/catalogue/partials/product.html#remove-from-basket",
					{"product": form.product},
				)
		return super().form_valid(form)

	def form_invalid(self, form):
		if self.request.htmx:
			message = _(
				"A problem occurred while trying to add the product to your cart. Try again later."
			)
			response = trigger_client_event(
				HttpResponse(status=HTTPStatus.NO_CONTENT),
				"showMessage",
				message,
			)
			return response
		return super().form_invalid(form)


class BasketRemoveView(HtmxModelActionView):
	model = Product
	action_class = BasketRemoveAction

	def get_template_names(self):
		return ["oscar/catalogue/partials/product.html#add-to-basket"]

	def get_action_kwargs(self):
		kwargs = super().get_action_kwargs()
		kwargs["product"] = self.object
		return kwargs

	def get_success_url(self):
		return self.request.path

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["product"] = self.object
		return context
