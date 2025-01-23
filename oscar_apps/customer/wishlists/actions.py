from django.http import Http404
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from htmx_utils import Action

from oscar_apps.wishlists.models import Line


class WishlistAddProductAction(Action):
	def action(self, wishlist, product):
		line, __ = wishlist.add(product)
		message = _("<strong>%s</strong> was added to your wish list.") % escape(
			product.get_title()
		)
		self.add_message(mark_safe(message))
		return line, product


class WishlistRemoveProductAction(Action):
	def action(self, wishlist, line_pk=None, product_pk=None):
		try:
			line, product = wishlist.remove(
				line_pk=line_pk, product_pk=product_pk, delete=True
			)
			line.pk = line_pk  # this is necessary as .delete() clears pk
		except Line.DoesNotExist as e:
			raise Http404 from e

		message = _("<strong>%s</strong> was removed from your wish list.") % escape(
			product.get_title()
		)
		self.add_message(mark_safe(message))
		return line, product
