from functools import cache

from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.utils.translation import gettext_lazy as _


class CountlessPage(Page):
	def __repr__(self):
		return "<Page %s>" % self.number

	@cache
	def has_next(self):
		return len(self.object_list) > len(self.object_list[: self.page_size])

	@cache
	def has_previous(self):
		return self.number > 1

	def has_other_pages(self):
		return self.has_next() or self.has_previous()

	def next_page_number(self):
		if self.has_next():
			return self.number + 1
		else:
			raise EmptyPage(_("Next page does not exist"))

	def previous_page_number(self):
		if self.has_previous():
			return self.number - 1
		else:
			raise EmptyPage(_("Previous page does not exist"))


class CountlessPaginator(Paginator):
	def validate_number(self, number):
		try:
			if isinstance(number, float) and not number.is_integer():
				raise ValueError
			number = int(number)
		except (TypeError, ValueError) as e:
			raise PageNotAnInteger(self.error_messages["invalid_page"]) from e
		if number < 1:
			raise EmptyPage(self.error_messages["min_page"])
		return number

	def get_page(self, number):
		try:
			number = self.validate_number(number)
		except (PageNotAnInteger, EmptyPage):
			number = 1
		return self.page(number)

	def page(self, number):
		number = self.validate_number(number)
		bottom = (number - 1) * self.per_page
		top = bottom + self.per_page + 1
		return CountlessPage(self.object_list[bottom:top], number, self.per_page)
