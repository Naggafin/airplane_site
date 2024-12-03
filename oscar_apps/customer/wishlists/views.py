from oscar.apps.customer.wishlists.views import (
	WishListListView as CoreWishListListView,
)


class WishListListView(CoreWishListListView):
	template_name = "pixio/shop-wishlist.html"
