from django import forms
from django.utils.translation import gettext_lazy as _
from oscar.apps.dashboard.partners.forms import *  # noqa: F403


class UserSearchForm(forms.Form):
	user = forms.CharField(
		label=_("Username or email address"),
		help_text=_(
			"A partial username or email address can be entered (eg '@example.com') to match multiple addresses."
		),
		max_length=100,
	)


class UpdateUserPermsForm(forms.Form):
	can_edit = forms.BooleanField(label=_("Can edit the store details"), required=False)
	can_delete = forms.BooleanField(
		label=_("Can delete the store (use caution!)"), required=False
	)
