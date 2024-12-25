from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from oscar.apps.wishlists.models import Line, WishList

from .constants import WISHLIST_CACHE_KEY


@receiver(post_save, sender=Line)
@receiver(post_delete, sender=Line)
@receiver(post_save, sender=WishList)
@receiver(post_delete, sender=WishList)
def handle_wishlist_change(sender, instance, **kwargs):
	"""
	Handle changes to wishlists or their lines to invalidate the cache.
	"""
	if isinstance(instance, WishList):
		user_id = instance.owner_id
	elif isinstance(instance, Line):
		user_id = instance.wishlist.owner_id
	else:
		return
	cache_key = WISHLIST_CACHE_KEY % user_id
	cache.delete(cache_key)
