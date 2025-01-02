import logging

from box import Box
from django.core.cache import cache
from django.core.signing import BadSignature, Signer

from .constants import BASKET_CACHE_KEY
from .middleware import BasketMiddleware
from .models import Basket
from .serializers import BasketSerializer

logger = logging.getLogger(__name__)

CACHE_TIMEOUT = 60 * 5  # 5 minutes


def get_or_create_basket_cache(request):
	"""
	Retrieve or create a cached basket for the given request.

	Returns:
	    dict: Serialized basket data or an empty list if no basket exists.
	"""

	def get_cache_key():
		if request.user.is_authenticated:
			return BASKET_CACHE_KEY % request.user.pk
		cookie_key = BasketMiddleware(None).get_cookie_key(request)
		return BASKET_CACHE_KEY % request.COOKIES.get(cookie_key, "")

	def fetch_basket():
		if request.user.is_authenticated:
			try:
				return Basket.objects.get(owner=request.user.pk)
			except Basket.MultipleObjectsReturned:
				logging.warning(f"Multiple baskets found for user #{request.user.pk}")
				return Basket.objects.filter(owner=request.user.pk).first()
		else:
			try:
				cookie_key = BasketMiddleware(None).get_cookie_key(request)
				basket_id = Signer().unsign(request.COOKIES.get(cookie_key, ""))
				return Basket.objects.get(pk=basket_id, owner=None, status=Basket.OPEN)
			except (BadSignature, Basket.DoesNotExist):
				return None

	cache_key = get_cache_key()
	cached_basket = cache.get(cache_key)

	if cached_basket:
		return Box(cached_basket)

	basket = fetch_basket()
	if not basket:
		return []

	serialized_basket = BasketSerializer(basket).data
	cache.set(cache_key, serialized_basket, timeout=CACHE_TIMEOUT)
	return Box(serialized_basket)
