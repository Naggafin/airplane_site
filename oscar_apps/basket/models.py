import auto_prefetch
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from oscar.apps.basket.abstract_models import (
	AbstractBasket,
	AbstractLine,
	AbstractLineAttribute,
)
from oscar.core.compat import AUTH_USER_MODEL


class Basket(auto_prefetch.Model, AbstractBasket):
	owner = auto_prefetch.ForeignKey(
		AUTH_USER_MODEL,
		null=True,
		related_name="baskets",
		on_delete=models.CASCADE,
		verbose_name=_("Owner"),
	)

	def remove(self, line_pk=None, product_pk=None, delete=False):
		"""
		Remove a product from this basket.
		"""

		# Fetch the line using the filter conditions in a manner that exploits cache
		lines = list(self.all_lines())

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

	class Meta(auto_prefetch.Model.Meta, AbstractBasket.Meta):
		pass


class Line(auto_prefetch.Model, AbstractLine):
	basket = auto_prefetch.ForeignKey(
		"basket.Basket",
		on_delete=models.CASCADE,
		related_name="lines",
		verbose_name=_("Basket"),
	)
	product = auto_prefetch.ForeignKey(
		"catalogue.Product",
		on_delete=models.CASCADE,
		related_name="basket_lines",
		verbose_name=_("Product"),
	)
	stockrecord = auto_prefetch.ForeignKey(
		"partner.StockRecord", on_delete=models.CASCADE, related_name="basket_lines"
	)

	@cached_property
	def max_allowed_quantity(self):
		num_available = getattr(self.purchase_info.availability, "num_available", None)
		basket_max_allowed_quantity = self.basket.max_allowed_quantity()[0]
		if all([num_available, basket_max_allowed_quantity]):
			max_allowed_quantity = min(num_available, basket_max_allowed_quantity)
		else:
			max_allowed_quantity = num_available or basket_max_allowed_quantity
		return max_allowed_quantity if max_allowed_quantity else None

	class Meta(auto_prefetch.Model.Meta, AbstractLine.Meta):
		pass


class LineAttribute(auto_prefetch.Model, AbstractLineAttribute):
	line = auto_prefetch.ForeignKey(
		"basket.Line",
		on_delete=models.CASCADE,
		related_name="attributes",
		verbose_name=_("Line"),
	)
	option = auto_prefetch.ForeignKey(
		"catalogue.Option", on_delete=models.CASCADE, verbose_name=_("Option")
	)

	class Meta(auto_prefetch.Model.Meta, AbstractLineAttribute.Meta):
		pass


from oscar.apps.basket.models import *  # noqa: F403, E402
