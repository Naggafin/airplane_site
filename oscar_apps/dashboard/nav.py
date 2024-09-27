from django.urls import resolve, reverse
from oscar.apps.dashboard.nav import _dashboard_url_names_to_config
from oscar.views.decorators import check_permissions


def access_fn(user, url_name, url_args=None, url_kwargs=None):
	if url_name is None:  # it's a heading
		return True

	url = reverse(url_name, args=url_args, kwargs=url_kwargs)
	url_match = resolve(url)
	url_name = url_match.url_name
	app_config_instance = _dashboard_url_names_to_config()[url_name]

	permissions = app_config_instance.get_permissions(url_name)

	return check_permissions(user, permissions)
