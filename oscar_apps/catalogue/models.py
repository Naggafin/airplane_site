from django.db import models
from django.utils.translation import gettext_lazy as _
from oscar.apps.catalogue.abstract_models import AbstractProduct
from taggit.managers import TaggableManager


class Product(AbstractProduct):
	video_url = models.URLField(_("video URL"), null=True)

	tags = TaggableManager()


from oscar.apps.catalogue.models import *  # noqa: F403, E402
