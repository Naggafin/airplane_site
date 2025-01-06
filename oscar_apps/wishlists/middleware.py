from django.utils.functional import SimpleLazyObject

from .utils import get_or_create_wishlist_cache


class WishListMiddleware:
	"""
	Middleware to fetch the cached wishlist for an authenticated user
	and attach it to the request object.
	"""

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		breakpoint()
		request.wishlist = SimpleLazyObject(lambda: self.get_wishlist(request))
		return self.get_response(request)

	def get_wishlist(self, request):
		return get_or_create_wishlist_cache(request)
