from django.utils.functional import SimpleLazyObject

from .utils import fetch_wishlist


class WishListMiddleware:
	"""
	Middleware to fetch the cached wishlist for an authenticated user
	and attach it to the request object.
	"""

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		request.wishlist = SimpleLazyObject(lambda: self.get_wishlist(request))
		return self.get_response(request)

	def get_wishlist(self, request):
		return fetch_wishlist(request)
