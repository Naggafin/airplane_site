from oscar.apps.checkout.views import IndexView as CoreIndexView


class IndexView(CoreIndexView):
	template_name = "pixio/shop-checkout.html"
