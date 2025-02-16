from djanfo.utils import timezone
from django.db.models import Q
from oscar.apps.catalogue.utils import *  # noqa: F403
from oscar.core.loading import get_model

ConditionalOffer = get_model("offer", "ConditionalOffer")


# TODO: to show discount previews, though this may be too complicated to implement right now
def get_global_offers(pks: list[int]):
	offers = (
		ConditionalOffer.objects.filter(
			(Q(start_datetime__isnull=True) | Q(start_datetime__lt=timezone.now()))
			& (Q(end_datetime__isnull=True) | Q(end_datetime__gt=timezone.now())),
			offer_type=ConditionalOffer.SITE,
			status=ConditionalOffer.OPEN,
		)
		.select_related("benefit", "condition__range")
		.filter(
			Q(condition__range__included_products__in=pks)
			| Q(condition__range__includes_all_products=True)
		)
	)
	return offers
