import oscar.apps.catalogue.apps as apps
from django.utils.translation import gettext_lazy as _


class CatalogueConfig(apps.CatalogueConfig):
	name = "oscar_apps.catalogue"
	verbose_name = _("Catalog")
