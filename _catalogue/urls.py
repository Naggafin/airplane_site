from django.urls import path

from . import views
from .models import Product, Review

app_name = "catalogue"

urlpatterns = [
	path(
		"list/",
		views.ProductCreateView.as_view(),
		name="create_%s" % Product._meta.model_name,
	),
	path(
		"update_listing/<pk:str>/",
		views.ProductUpdateView.as_view(),
		name="update_%s" % Product._meta.model_name,
	),
	path(
		"review/<pk:str>/",
		views.ReviewCreateView.as_view(),
		name="create_%s" % Review._meta.model_name,
	),
	path(
		"update_review/<pk:str>/",
		views.ReviewUpdateView.as_view(),
		name="update_%s" % Review._meta.model_name,
	),
]
