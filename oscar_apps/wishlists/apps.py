import oscar.apps.wishlists.apps as apps


class WishlistsConfig(apps.WishlistsConfig):
	name = "oscar_apps.wishlists"

	def ready(self):
		super().ready()
