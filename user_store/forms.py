from django import forms
from oscar.apps.partner.models import Partner


class PartnerForm(forms.ModelForm):
	class Meta:
		model = Partner
		fields = ["name"]
