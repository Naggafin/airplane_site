from django.db.models import Sum
from haystack import indexes
from oscar.apps.search.search_indexes import ProductIndex as CoreProductIndex
from oscar.core.loading import get_model

Line = get_model("order", "Line")


class ProductIndex(CoreProductIndex):
	num_purchases = indexes.IntegerField(null=True, faceted=True)

	def prepare_num_purchases(self, obj):
		return (
			Line.objects.filter(product=obj, order__status="Complete").aggregate(
				total_purchased=Sum("quantity")
			)["total_purchased"]
			or 0
		)
