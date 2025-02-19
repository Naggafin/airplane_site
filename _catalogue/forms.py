from django import forms

from .models import Product, Review


class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ["title", "upc", "description", "price"]


class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ["rating", "comment"]
