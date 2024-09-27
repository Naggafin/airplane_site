from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from oscar.apps.catalogue.models import Product
from oscar.apps.partner.models import Partner

from .forms import PartnerForm


class RegisterView(CreateView):
	form_class = PartnerForm
	success_url = reverse_lazy("dashboard")

	def form_valid(self, form):
		partner = form.save()
		partner.users.add(self.request.user)
		partner.save()
		return super().form_valid(form)


class PartnerStoreView(TemplateView):
	template_name = "user_store/partner_store.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		partner_id = self.kwargs.get("partner_id")
		partner = get_object_or_404(Partner, id=partner_id)
		products = Product.objects.filter(stockrecords__partner=partner)
		context["partner"] = partner
		context["products"] = products
		return context
