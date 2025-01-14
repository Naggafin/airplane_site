import oscar.apps.basket.apps as apps
from django.contrib.auth.decorators import login_required
from django.urls import path
from oscar.core.loading import get_class


class BasketConfig(apps.BasketConfig):
	name = "oscar_apps.basket"

	def ready(self):
		super().ready()
		self.update_view = get_class("basket.views", "BasketLineUpdate")
		self.remove_view = get_class("basket.views", "BasketLineRemove")

	def get_urls(self):
		urls = [
			path("", self.summary_view.as_view(), name="summary"),
			path("add/<int:pk>/", self.add_view.as_view(), name="add-product"),
			path("update/<int:pk>/", self.update_view.as_view(), name="update-line"),
			path("remove/<int:pk>/", self.remove_view.as_view(), name="remove-line"),
			path(
				"remove/<int:pk>/",
				self.remove_view.as_view(),
				name="remove-product",
			),
			path("vouchers/add/", self.add_voucher_view.as_view(), name="vouchers-add"),
			path(
				"vouchers/<int:pk>/remove/",
				self.remove_voucher_view.as_view(),
				name="vouchers-remove",
			),
			path("saved/", login_required(self.saved_view.as_view()), name="saved"),
		]
		return self.post_process_urls(urls)
