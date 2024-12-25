from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from oscar.apps.basket.models import Basket, Line

from .constants import BASKET_CACHE_KEY


@receiver(post_save, sender=Line)
@receiver(post_delete, sender=Line)
@receiver(post_save, sender=Basket)
@receiver(post_delete, sender=Basket)
def handle_wishlist_change(sender, instance, **kwargs):
	"""
	Handle changes to baskets or their lines to invalidate the cache.
	"""
	if isinstance(instance, Basket):
		user_id = instance.owner_id
	elif isinstance(instance, Line):
		user_id = instance.basket.owner_id
	else:
		return
	cache_key = BASKET_CACHE_KEY % user_id
	cache.delete(cache_key)
