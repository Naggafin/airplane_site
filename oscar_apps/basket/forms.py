from django import forms
from django.utils.translation import gettext_lazy as _
from django_fastdev.apps import fastdev_ignore
from oscar.apps.basket.forms import AddToBasketForm


@fastdev_ignore
class SimpleAddToBasketForm(AddToBasketForm):
	quantity = forms.IntegerField(
		initial=1, min_value=1, label=_("Quantity"), widget=forms.HiddenInput
	)

	def __init__(self, basket, product, *args, **kwargs):
		# fixed to not dynamically populate with more fields
		self.basket = basket
		self.parent_product = product
		super(forms.Form, self).__init__(*args, **kwargs)
