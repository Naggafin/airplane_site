from django.urls import path

from .views import PartnerStoreView

urlpatterns = [
	path("store/<int:partner_id>/", PartnerStoreView.as_view(), name="partner_store"),
]
