from django.forms import Form
from django_fastdev.apps import fastdev_ignore
from oscar.apps.basket.forms import (
	SimpleAddToBasketForm as CoreSimpleAddToBasketForm,
)


@fastdev_ignore
class SimpleAddToBasketForm(CoreSimpleAddToBasketForm):
	def __init__(self, basket, product, *args, **kwargs):
		# fixed to not dynamically populate with more fields
		self.basket = basket
		self.parent_product = product
		super(Form, self).__init__(*args, **kwargs)
