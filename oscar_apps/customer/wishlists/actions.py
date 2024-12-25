from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from htmx_utils import Action

from oscar_apps.wishlists.models import Line


class WishlistAddProductAction(Action):
	def action(self, wishlist, product):
		wishlist.add(product)
		message = _("<strong>%s</strong> was added to your wish list.") % escape(
			product.get_title()
		)
		self.add_message(mark_safe(message))


class WishlistRemoveProductAction(Action):
	def action(self, wishlist_key, line_pk=None, product_pk=None):
		line, product, wishlist = self.fetch_line(
			self.request.user, wishlist_key, line_pk, product_pk
		)
		line.delete()
		message = _("<strong>%s</strong> was removed from your wish list.") % escape(
			product.get_title()
		)
		self.add_message(mark_safe(message))
		return product, wishlist

	def fetch_line(self, user, wishlist_key, line_pk=None, product_pk=None):
		if line_pk is not None:
			line = get_object_or_404(
				Line,
				pk=line_pk,
				wishlist__owner=user,
				wishlist__key=wishlist_key,
			)
		else:
			try:
				line = get_object_or_404(
					Line,
					product_id=product_pk,
					wishlist__owner=user,
					wishlist__key=wishlist_key,
				)
			except Line.MultipleObjectsReturned as e:
				raise Http404 from e
		wishlist = line.wishlist
		product = line.product
		return line, product, wishlist
