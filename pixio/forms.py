from django import forms


class ContactusForm(forms.Form):
	name = forms.CharField(max_length=255, required=False)
	email = forms.EmailField()
	content = forms.CharField(widget=forms.Textarea)
