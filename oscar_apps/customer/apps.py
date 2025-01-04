import oscar.apps.customer.apps as apps
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views import generic
from oscar.core.loading import get_class


class CustomerConfig(apps.CustomerConfig):
	name = "oscar_apps.customer"

	def ready(self):
		super().ready()
		self.wishlists_update_line_view = get_class(
			"customer.wishlists.views", "WishListUpdateLine"
		)

	def get_urls(self):
		urls = [
			path("", login_required(self.summary_view.as_view()), name="summary"),
			# Profile
			path(
				"profile/",
				login_required(self.profile_view.as_view()),
				name="profile-view",
			),
			path(
				"profile/edit/",
				login_required(self.profile_update_view.as_view()),
				name="profile-update",
			),
			path(
				"profile/delete/",
				login_required(self.profile_delete_view.as_view()),
				name="profile-delete",
			),
			# Order history
			path(
				"orders/",
				login_required(self.order_history_view.as_view()),
				name="order-list",
			),
			re_path(
				r"^order-status/(?P<order_number>[\w-]*)/(?P<hash>[A-z0-9-_=:]+)/$",
				self.anon_order_detail_view.as_view(),
				name="anon-order",
			),
			path(
				"orders/<str:order_number>/",
				login_required(self.order_detail_view.as_view()),
				name="order",
			),
			path(
				"orders/<str:order_number>/<int:line_id>/",
				login_required(self.order_line_view.as_view()),
				name="order-line",
			),
			# Address book
			path(
				"addresses/",
				login_required(self.address_list_view.as_view()),
				name="address-list",
			),
			path(
				"addresses/add/",
				login_required(self.address_create_view.as_view()),
				name="address-create",
			),
			path(
				"addresses/<int:pk>/",
				login_required(self.address_update_view.as_view()),
				name="address-detail",
			),
			path(
				"addresses/<int:pk>/delete/",
				login_required(self.address_delete_view.as_view()),
				name="address-delete",
			),
			re_path(
				r"^addresses/(?P<pk>\d+)/(?P<action>default_for_(billing|shipping))/$",
				login_required(self.address_change_status_view.as_view()),
				name="address-change-status",
			),
			# Email history
			path(
				"emails/",
				login_required(self.email_list_view.as_view()),
				name="email-list",
			),
			path(
				"emails/<int:email_id>/",
				login_required(self.email_detail_view.as_view()),
				name="email-detail",
			),
			# Notifications
			# Redirect to notification inbox
			path(
				"notifications/",
				generic.RedirectView.as_view(
					url="/accounts/notifications/inbox/", permanent=False
				),
			),
			path(
				"notifications/inbox/",
				login_required(self.notification_inbox_view.as_view()),
				name="notifications-inbox",
			),
			path(
				"notifications/archive/",
				login_required(self.notification_archive_view.as_view()),
				name="notifications-archive",
			),
			path(
				"notifications/update/",
				login_required(self.notification_update_view.as_view()),
				name="notifications-update",
			),
			path(
				"notifications/<int:pk>/",
				login_required(self.notification_detail_view.as_view()),
				name="notifications-detail",
			),
			# Alerts
			# Alerts can be setup by anonymous users: some views do not
			# require login
			path(
				"alerts/",
				login_required(self.alert_list_view.as_view()),
				name="alerts-list",
			),
			path(
				"alerts/create/<int:pk>/",
				self.alert_create_view.as_view(),
				name="alert-create",
			),
			path(
				"alerts/confirm/<str:key>/",
				self.alert_confirm_view.as_view(),
				name="alerts-confirm",
			),
			path(
				"alerts/cancel/key/<str:key>/",
				self.alert_cancel_view.as_view(),
				name="alerts-cancel-by-key",
			),
			path(
				"alerts/cancel/<int:pk>/",
				login_required(self.alert_cancel_view.as_view()),
				name="alerts-cancel-by-pk",
			),
			# Wishlists
			path(
				"wishlist/",
				login_required(self.wishlists_detail_view.as_view()),
				name="wishlist-detail",
			),
			path(
				"wishlist/<str:key>/",
				self.wishlists_detail_view.as_view(),
				name="wishlist-detail",
			),
			path(
				"wishlist/add/<int:product_pk>/",
				login_required(self.wishlists_add_product_view.as_view()),
				name="wishlist-add-product",
			),
			path(
				"wishlist/lines/<int:line_pk>/update/",
				login_required(self.wishlists_update_line_view.as_view()),
				name="wishlist-update-line",
			),
			path(
				"wishlist/lines/<int:line_pk>/delete/",
				login_required(self.wishlists_remove_product_view.as_view()),
				name="wishlist-remove-product",
			),
			path(
				"wishlist/products/<int:product_pk>/delete/",
				login_required(self.wishlists_remove_product_view.as_view()),
				name="wishlist-remove-product",
			),
		]

		return self.post_process_urls(urls)
