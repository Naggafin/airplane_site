import django.dispatch
from django.core.cache import cache
from django.dispatch import receiver
from oscar.apps.basket.signals import *  # noqa: F403

from .utils import get_cache_key

basket_changed = django.dispatch.Signal()


@receiver(basket_changed)
@receiver(basket_addition)  # noqa: F405
def handle_basket_change(sender, product, user, request, **kwargs):
	cache_key = get_cache_key(request)
	cache.delete(cache_key)
