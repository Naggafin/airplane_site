import django_tables2 as tables
from django.shortcuts import render
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from oscar.core.thumbnails import get_thumbnailer
from oscar.templatetags.currency_filters import currency
from oscar.templatetags.purchase_info_tags import purchase_info_for_product

from .models import Line


class LineTable(tables.Table):
	THUMBNAIL_SIZE = "100x100"
	PARTIALS_PATH = "oscar/wishlists/partials/wishlist_table_columns.html"

	# Define unique CSS classes for each column
	column_class_map = {
		"product_image": "product-item-img",
		"product_title": "product-item-name",
		"product_price": "product-item-price",
		"product_stock": "product-item-stock",
		"quantity": "",
		"line_add": "product-item-totle",
		"line_remove": "product-item-close",
	}

	product_image = tables.Column(
		verbose_name=_("Product"), empty_values=(), orderable=False
	)
	product_title = tables.Column(
		verbose_name="",
		accessor="product__get_title",
		linkify=lambda record: record.product.get_absolute_url(),
		order_by="product__title",
	)
	product_price = tables.Column(verbose_name=_("Price"), empty_values=())
	product_stock = tables.Column(verbose_name=_("Stock"), empty_values=())
	quantity = tables.Column(verbose_name=_("Quantity"))
	line_add = tables.Column(verbose_name="", empty_values=(), orderable=False)
	line_remove = tables.Column(verbose_name="", empty_values=(), orderable=False)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for column_name, column in self.base_columns.items():
			column.attrs = column.attrs or {}
			column.attrs["td"] = {"class": self.column_class_map.get(column_name, "")}

	def order_product_price(self, queryset, is_descending):
		# TODO
		return queryset

	def order_product_stock(self, queryset, is_descending):
		# TODO
		return queryset

	def render_product_image(self, record):
		product = record.product
		image = product.primary_image()
		original = image["original"] if isinstance(image, dict) else image.original
		caption = (
			image["caption"] if isinstance(image, dict) else image.caption
		) or product.get_title()
		thumbnail = get_thumbnailer().generate_thumbnail(
			original, size=self.THUMBNAIL_SIZE
		)
		return format_html('<img src="{}" alt="{}">', thumbnail.url, caption)

	def render_product_price(self, record):
		session = purchase_info_for_product(self.request, record.product)
		if not session.price.exists:
			return "&nbsp;"

		price = (
			currency(session.price.incl_tax, session.price.currency)
			if session.price.is_tax_known
			else currency(session.price.excl_tax, session.price.currency)
		)

		# TODO: Replace with actual discount logic
		discount_price = None
		if discount_price:
			return format_html(
				'<span class="text-decoration-line-through">{}</span> <strong>{}</strong>',
				price,
				discount_price,
			)

		return price or _("Free")

	def render_product_stock(self, record):
		availability = purchase_info_for_product(
			self.request, record.product
		).availability
		return _("In Stock") if availability.is_available_to_buy else _("Unavailable")

	def _render_partial(self, partial_id: str, context: dict) -> str:
		"""Helper to render partial templates."""
		return mark_safe(
			render(
				self.request,
				f"{self.PARTIALS_PATH}#{partial_id}",
				context,
			).content.decode()
		)

	def render_quantity(self, record):
		context = {"line": record, "product": record.product}
		return self._render_partial("quantity", context)

	def render_line_add(self, record):
		context = {"line": record, "product": record.product}
		return self._render_partial("add", context)

	def render_line_remove(self, record):
		context = {"line": record, "product": record.product}
		return self._render_partial("remove", context)

	class Meta:
		model = Line
		template_name = "django_tables2/bootstrap5-responsive-htmx.html"
		empty_text = _("You have no products in your wishlist.")
		fields = (
			"product_image",
			"product_title",
			"product_price",
			"product_stock",
			"quantity",
			"line_add",
			"line_remove",
		)
		sequence = (
			"product_image",
			"product_title",
			"product_price",
			"product_stock",
			"quantity",
			"line_add",
			"line_remove",
		)
		attrs = {"class": "table check-tbl style-1"}
		row_attrs = {"x-data": lambda record: "{quantity: %d}" % record.quantity}
