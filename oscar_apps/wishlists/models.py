from oscar.apps.wishlists.abstract_models import AbstractWishList
from oscar.apps.wishlists.models import Line


class WishList(AbstractWishList):
	def remove(self, line_pk=None, product_pk=None, delete=False):
		"""
		Remove a product from this wishlist.
		"""
		# Determine filter condition based on provided primary key or product
		filter_conditions = {"pk": line_pk} if line_pk else {"product_id": product_pk}

		# Fetch the line using the filter conditions and prefetch product details
		line = self.lines.select_related("product").get(**filter_conditions)
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

	def merge_line(self, line, add_quantities=True):
		"""
		For transferring a line from another wishlist to this one.
		"""
		try:
			existing_line = self.lines.get(product=line.product_id)
		except Line.DoesNotExist:
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


from oscar.apps.wishlists.models import *  # noqa: E402, F403
