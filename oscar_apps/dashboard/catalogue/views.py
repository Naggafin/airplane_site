from oscar.apps.dashboard.catalogue.views import *  # noqa: F403

"""
class ProductCreateUpdateView(OscarProductCreateUpdateView):
    def get_queryset(self):
        \"\"\"
        Filter products to only those owned by the user's associated partner.
        \"\"\"
        qs = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_superuser and hasattr(self.request.user, 'partners'):
            qs = qs.filter(stockrecords__partner__in=self.request.user.partners.all())
        return qs
"""
