from http import HTTPStatus

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView
from django_htmx.http import trigger_client_event
from htmx_utils.views import HtmxActionView
from htmx_utils.views.mixins import HtmxFormMixin
from oscar.apps.basket.utils import BasketMessageGenerator
from oscar.apps.basket.views import (
	BasketAddView as CoreBasketAddView,
	BasketView as CoreBasketView,
)

from .actions import BasketRemoveLineAction
from .forms import BasketLineForm
from .models import Line


class BasketView(CoreBasketView):
	template_name = "pixio/shop-cart.html"


class BasketAddView(CoreBasketAddView):
	def form_valid(self, form):
		offers_before = self.request.basket.applied_offers()

		line, __ = self.request.basket.add_product(
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
			context = {
				"line": line,
				"product": form.product,
			}
			return render(
				self.request,
				"oscar/basket/partials/basket_line_add_partial.html",
				context,
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


class BasketLineUpdate(HtmxFormMixin, UpdateView):
	model = Line
	form_class = BasketLineForm

	def get(self, request, *args, **kwargs):
		return redirect(self.get_success_url())

	def get_queryset(self):
		return self.request.basket.lines.all()

	def get_success_url(self):
		return reverse("basket:summary")

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
				"oscar/basket/partials/basket_line_remove_partial.html"
				if deleted
				else "oscar/basket/partials/basket_line_update_partial.html"
			)
			return render(self.request, template, context)
		return redirect(self.get_success_url())


class BasketLineRemove(HtmxActionView):
	action_class = BasketRemoveLineAction

	def get(self, request, *args, **kwargs):
		return redirect(self.get_success_url())

	def get_template_names(self):
		return ["oscar/basket/partials/basket_line_remove_partial.html"]

	def get_action_kwargs(self):
		kwargs = super().get_action_kwargs()
		kwargs["line_pk"] = self.kwargs.get("line_pk")
		kwargs["product_pk"] = self.kwargs.get("product_pk")
		kwargs["basket"] = self.request.basket
		return kwargs

	def get_success_url(self):
		return reverse("basket:summary")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		line, product = self.action.result
		context["line"] = line
		context["product"] = product
		return context
