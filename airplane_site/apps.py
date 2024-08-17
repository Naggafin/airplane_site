from oscar import config
from django.urls import include, path

class AircraftShopConfig(config.Shop):
	name = "airplane_site"
	
	# Override get_urls method
	def get_urls(self):
		urlpatterns = [
			path('catalog/', self.catalogue_app.urls)
		] + super().get_urls()
		return urlpatterns
