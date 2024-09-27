from django.conf import settings
from django.utils.translation import gettext_lazy as _
from oscar.apps.catalogue.abstract_models import AbstractProduct


class Product(AbstractProduct):
	listed_by = models.ForeignKey(
		settings.AUTH_USER_MODEL, verbose_name=_("listed by"), on_delete=models.CASCADE
	)
	video_url = models.URLField(_("video URL"), null=True)


from oscar.apps.catalogue.models import *  # noqa
