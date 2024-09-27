from oscar.apps.dashboard.catalogue import forms as base_forms


class ProductForm(base_forms.ProductForm):
	class Meta(base_forms.ProductForm.Meta):
		fields = list(base_forms.ProductForm.Meta.fields) + ["video_url"]
