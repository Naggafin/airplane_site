import django_filters
from oscar.core.loading import get_model

Product = get_model("catalogue", "Product")


class ProductFilter(django_filters.FilterSet):
	price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
	price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
	category = django_filters.ModelChoiceFilter(
		queryset=Product.objects.values_list("category", flat=True).distinct()
	)
	title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

	class Meta:
		model = Product
		fields = ["price_min", "price_max", "category", "title"]
