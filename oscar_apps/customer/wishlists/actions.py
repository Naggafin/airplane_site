from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from htmx_utils import Action


class WishlistAddProductAction(Action):
	def action(self, wishlist, product):
		wishlist.add(product)
		message = _("<strong>%s</strong> was added to your wish list.") % escape(
			product.get_title()
		)
		self.add_message(mark_safe(message))


class WishlistRemoveProductAction(Action):
	def action(self, wishlist, line_pk=None, product_pk=None):
		line, product = wishlist.remove(
			line_pk=line_pk, product_pk=product_pk, delete=True
		)
		message = _("<strong>%s</strong> was removed from your wish list.") % escape(
			product.get_title()
		)
		self.add_message(mark_safe(message))
		return product
