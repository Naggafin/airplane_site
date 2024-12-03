from oscar.apps.catalogue.views import (
	CatalogueView as CoreCatalogueView,
	ProductDetailView as CoreProductDetailView,
)


class ProductDetailView(CoreProductDetailView):
	template_name = "pixio/product.html"

	def get_template_names(self):
		if self.request.htmx:
			return ["pixio/index.html#productModal"]
		return super().get_template_names()


class CatalogueView(CoreCatalogueView):
	template_name = "pixio/shop.html"
