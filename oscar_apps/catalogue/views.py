from oscar.apps.catalogue.views import (
	ProductDetailView as CoreProductDetailView,
)
from oscar.core.loading import get_class


class ProductDetailView(CoreProductDetailView):
	template_name = "pixio/product.html"

	def get_template_names(self):
		if self.request.htmx:
			if self.request.htmx.target == "modalContainer":
				return ["pixio/index.html#product-modal"]
		return super().get_template_names()


CatalogueView = get_class("search.views", "CatalogueView")
ProductCategoryView = get_class("search.views", "ProductCategoryView")
