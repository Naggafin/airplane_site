from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext_lazy
from htmx_utils import Action


class BasketRemoveAction(Action):
	def action(self, product):
		basket = self.request.basket
		quantity = basket.lines.filter(product=product).delete()[0]
		message = ngettext_lazy(
			"<strong>%(product)s</strong> has been added to your removed.",
			"<strong>%(quantity)d</strong> copies of <strong>%(product)s</strong> have been removed to your basket.",
			"quantity",
		)
		self.add_message(
			mark_safe(
				message % {"quantity": quantity, "product": escape(product.get_title())}
			)
		)
		return
