from django.http import Http404
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext_lazy
from htmx_utils import Action

from .models import Line


class BasketRemoveLineAction(Action):
	def action(self, basket, line_pk=None, product_pk=None):
		try:
			line, product = basket.remove(
				line_pk=line_pk, product_pk=product_pk, delete=True
			)
		except Line.DoesNotExist as e:
			raise Http404 from e

		message = ngettext_lazy(
			"<strong>%(product)s</strong> has been added to your removed.",
			"<strong>%(quantity)d</strong> copies of <strong>%(product)s</strong> have been removed to your basket.",
			"quantity",
		)
		self.add_message(
			mark_safe(
				message
				% {"quantity": line.quantity, "product": escape(product.get_title())}
			)
		)
		return line, product
