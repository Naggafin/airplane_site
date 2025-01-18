import auto_prefetch
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from oscar.apps.wishlists.abstract_models import AbstractLine, AbstractWishList
from oscar.core.compat import AUTH_USER_MODEL


class WishList(auto_prefetch.Model, AbstractWishList):
	owner = auto_prefetch.ForeignKey(
		AUTH_USER_MODEL,
		related_name="wishlists",
		on_delete=models.CASCADE,
		verbose_name=_("Owner"),
	)

	def __str__(self):
		return _("%s's Wishlist") % self.owner

	def get_absolute_url(self):
		return reverse("customer:wishlist-detail", kwargs={"key": self.key})

	def add(self, product):
		"""
		Add a product to this wishlist
		"""
		lines = self.lines.filter(product=product)
		if len(lines) == 0:
			created = True
			line = self.lines.create(product=product, title=product.get_title())
		else:
			created = False
			line = lines[0]
			line.quantity += 1
			line.save()
		return line, created

	def remove(self, line_pk=None, product_pk=None, delete=False):
		"""
		Remove a product from this wishlist.
		"""

		# Fetch the line using the filter conditions in a manner that exploits cache
		lines = list(self.lines.all())

		try:
			line = [
				line
				for line in lines
				if line.pk == line_pk or line.product_id == product_pk
			][0]
		except IndexError as e:
			raise Line.DoesNotExist from e

		product = line.product

		# Handle deletion or quantity adjustment
		if delete:
			line.delete()
		else:
			# Decrease quantity, delete if zero or save if greater than zero
			line.quantity = max(0, line.quantity - 1)
			if line.quantity > 0:
				line.save()
			else:
				line.delete()

		return line, product

	remove.alters_data = True

	def merge_line(self, line, add_quantities=True):
		"""
		For transferring a line from another wishlist to this one.
		"""
		try:
			existing_lines = list(self.lines.all())
			existing_line = [
				existing_line
				for existing_line in existing_lines
				if existing_line.product_id == line.product_id
			][0]
		except IndexError:
			# Line does not already exist - reassign its wishlist
			line.wishlist = self
			line.save()
		else:
			# Line already exists - assume the max quantity is correct and
			# delete the old
			if add_quantities:
				existing_line.quantity += line.quantity
			else:
				existing_line.quantity = max(existing_line.quantity, line.quantity)
			existing_line.save()
			line.delete()

	merge_line.alters_data = True

	def merge(self, wishlist, add_quantities=True):
		"""
		Merges another wishlist with this one.

		:wishlist: The wishlist to merge into this one.
		:add_quantities: Whether to add line quantities when they are merged.
		"""
		# Use wishlist.lines.all instead of all_lines as this function is called
		# before a strategy has been assigned.
		for line_to_merge in wishlist.lines.all():
			self.merge_line(line_to_merge, add_quantities)
		wishlist.delete()

	merge.alters_data = True

	class Meta(auto_prefetch.Model.Meta, AbstractWishList.Meta):
		pass


class Line(auto_prefetch.Model, AbstractLine):
	wishlist = auto_prefetch.ForeignKey(
		"wishlists.WishList",
		on_delete=models.CASCADE,
		related_name="lines",
		verbose_name=_("Wish List"),
	)
	product = auto_prefetch.ForeignKey(
		"catalogue.Product",
		verbose_name=_("Product"),
		related_name="wishlists_lines",
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
	)

	class Meta(auto_prefetch.Model.Meta, AbstractLine.Meta):
		pass


from oscar.apps.wishlists.models import *  # noqa: E402, F403
