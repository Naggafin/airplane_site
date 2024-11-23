import oscar.apps.dashboard.apps as apps
from django.urls import include, path, reverse
from django.views.generic import RedirectView


class DashboardConfig(apps.DashboardConfig):
	name = "oscar_apps.dashboard"

	def get_urls(self):
		urls = [
			path("", self.index_view.as_view(), name="index"),
			path("catalogue/", include(self.catalogue_app.urls[0])),
			path("reports/", include(self.reports_app.urls[0])),
			path("orders/", include(self.orders_app.urls[0])),
			path("users/", include(self.users_app.urls[0])),
			path("pages/", include(self.pages_app.urls[0])),
			path("partners/", include(self.partners_app.urls[0])),
			path("offers/", include(self.offers_app.urls[0])),
			path("ranges/", include(self.ranges_app.urls[0])),
			path("reviews/", include(self.reviews_app.urls[0])),
			path("vouchers/", include(self.vouchers_app.urls[0])),
			path("comms/", include(self.comms_app.urls[0])),
			path("shipping/", include(self.shipping_app.urls[0])),
			path(
				"login/",
				RedirectView.as_view(pattern_name="account_login", permanent=True),
				name="login",
			),
			path(
				"logout/",
				RedirectView.as_view(pattern_name="account_logout", permanent=True),
				name="logout",
			),
		]
		return self.post_process_urls(urls)
