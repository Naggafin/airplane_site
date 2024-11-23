from django.apps import apps
from django.conf import settings
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView
from oscar import config
from oscar.core.application import OscarConfig
from oscar.core.loading import get_class


class AircraftShopConfig(config.Shop):
	name = "airplane_site"

	# Override get_urls method
	def get_urls(self):
		urls = [
			path("", RedirectView.as_view(url=settings.OSCAR_HOMEPAGE), name="home"),
			path("catalog/", self.catalogue_app.urls),
			path("basket/", self.basket_app.urls),
			path("checkout/", self.checkout_app.urls),
			path("accounts/", self.customer_app.urls),
			path("search/", self.search_app.urls),
			path("dashboard/", self.dashboard_app.urls),
			path("offers/", self.offer_app.urls),
			path("wishlists/", self.wishlists_app.urls),
		]
		return urlpatterns
