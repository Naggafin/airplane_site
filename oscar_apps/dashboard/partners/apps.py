import oscar.apps.dashboard.partners.apps as apps
from django.urls import path


class PartnersDashboardConfig(apps.PartnersDashboardConfig):
	name = "oscar_apps.dashboard.partners"
	permissions_map = {
		"partner-list": (["is_staff"], ["partner.dashboard_access"]),
		"partner-create": (["is_staff"], ["partner.add_partner"]),
		"partner-manage": (["is_staff"], ["partner.dashboard_access"]),
		"partner-delete": (["is_staff"], ["partner.dashboard_access"]),
		"partner-user-select": (["is_staff"], ["partner.dashboard_access"]),
		"partner-user-link": (["is_staff"], ["partner.dashboard_access"]),
		"partner-user-unlink": (["is_staff"], ["partner.dashboard_access"]),
		"partner-user-update": (["is_staff"], ["partner.dashboard_access"]),
	}

	def get_urls(self):
		urls = [
			path("", self.list_view.as_view(), name="partner-list"),
			path("create/", self.create_view.as_view(), name="partner-create"),
			path("<int:pk>/", self.manage_view.as_view(), name="partner-manage"),
			path("<int:pk>/delete/", self.delete_view.as_view(), name="partner-delete"),
			path(
				"<int:partner_pk>/users/select/",
				self.user_select_view.as_view(),
				name="partner-user-select",
			),
			path(
				"<int:partner_pk>/users/<int:user_pk>/link/",
				self.user_link_view.as_view(),
				name="partner-user-link",
			),
			path(
				"<int:partner_pk>/users/<int:user_pk>/unlink/",
				self.user_unlink_view.as_view(),
				name="partner-user-unlink",
			),
			path(
				"<int:partner_pk>/users/<int:user_pk>/update/",
				self.user_update_view.as_view(),
				name="partner-user-update",
			),
		]
		return self.post_process_urls(urls)
