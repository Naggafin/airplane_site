from django.contrib import messages
from django.contrib.auth import get_permission_codename
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from guardian.mixins import PermissionListMixin, PermissionRequiredMixin
from guardian.shortcuts import assign_perm, remove_perm
from oscar.apps.dashboard.partners.views import (  # PartnerUserUpdateView as OscarPartnerUserUpdateView,
    PartnerCreateView as OscarPartnerCreateView,
    PartnerDeleteView as OscarPartnerDeleteView,
    PartnerListView as OscarPartnerListView,
    PartnerManageView as OscarPartnerManageView,
    PartnerUserLinkView as OscarPartnerUserLinkView,
    PartnerUserSelectView as OscarPartnerUserSelectView,
    PartnerUserUnlinkView as OscarPartnerUserUnlinkView,
)
from oscar.apps.partner.models import Partner
from oscar.core.compat import get_user_model

from .forms import UpdateUserPermsForm, UserSearchForm

User = get_user_model()


class PartnerListView(PermissionListMixin, OscarPartnerListView):
	permission_required = (
		Partner._meta.app_label + "." + get_permission_codename("view", Partner._meta)
	)

	def check_permissions(self, request):
		obj = self.get_permission_object()
		if obj.users.filter(pk=request.user.pk).exists():
			return None  # None = pass
		return super().check_permissions(request)


class PartnerCreateView(PermissionRequiredMixin, OscarPartnerCreateView):
	permission_required = (
		Partner._meta.app_label + "." + get_permission_codename("add", Partner._meta)
	)
	return_403 = True
	accept_global_perms = True


class PartnerManageView(PermissionRequiredMixin, OscarPartnerManageView):
	permission_required = (
		Partner._meta.app_label + "." + get_permission_codename("change", Partner._meta)
	)
	return_403 = True

	def get_permission_object(self):
		partner_pk = self.kwargs.get("pk")
		partner = get_object_or_404(Partner, pk=partner_pk)
		return partner


class PartnerDeleteView(PermissionRequiredMixin, OscarPartnerDeleteView):
	permission_required = (
		Partner._meta.app_label + "." + get_permission_codename("delete", Partner._meta)
	)
	return_403 = True


class PartnerUserSelectView(OscarPartnerUserSelectView):
	form_class = UserSearchForm
	permission_required = (
		Partner._meta.app_label + "." + get_permission_codename("change", Partner._meta)
	)
	return_403 = True

	def get(self, request, *args, **kwargs):
		data = None
		if "user" in request.GET:
			data = request.GET
		self.form = self.form_class(data)
		return super(OscarPartnerUserSelectView, self).get(request, *args, **kwargs)

	def get_queryset(self):
		if self.form.is_valid():
			search = self.request.GET.get("user")
			return User.objects.filter(
				Q(username__icontains=search) | Q(email__icontains=search)
			)
		else:
			return User.objects.none()

	def get_permission_object(self):
		return self.partner


class PartnerUserLinkView(PermissionRequiredMixin, OscarPartnerUserLinkView):
	permission_required = (
		Partner._meta.app_label + "." + get_permission_codename("change", Partner._meta)
	)
	return_403 = True

	def get_permission_object(self):
		partner_pk = self.kwargs.get("partner_pk")
		partner = get_object_or_404(Partner, pk=partner_pk)
		return partner

	def link_user(self, user, partner):
		if not super().link_user(user, partner):
			return False
		permission = (
			Partner._meta.app_label
			+ "."
			+ get_permission_codename("view", Partner._meta)
		)
		assign_perm(permission, user, partner)
		return True


class PartnerUserUnlinkView(PermissionRequiredMixin, OscarPartnerUserUnlinkView):
	permission_required = (
		Partner._meta.app_label + "." + get_permission_codename("change", Partner._meta)
	)
	return_403 = True

	def get_permission_object(self):
		partner_pk = self.kwargs.get("partner_pk")
		partner = get_object_or_404(Partner, pk=partner_pk)
		return partner

	def unlink_user(self, user, partner):
		if not super().unlink_user(user, partner):
			return False
		for permission in (
			Partner._meta.app_label
			+ "."
			+ get_permission_codename("view", Partner._meta),
			Partner._meta.app_label
			+ "."
			+ get_permission_codename("change", Partner._meta),
			Partner._meta.app_label
			+ "."
			+ get_permission_codename("delete", Partner._meta),
		):
			remove_perm(permission, user, partner)
		return True


class PartnerUserUpdateView(PermissionRequiredMixin, FormView):
	template_name = "oscar/dashboard/partners/partner_user_form.html"
	form_class = UpdateUserPermsForm
	permission_required = (
		Partner._meta.app_label
		+ "."
		+ get_permission_codename("change", Partner._meta),
		Partner._meta.app_label
		+ "."
		+ get_permission_codename("delete", Partner._meta),
	)
	return_403 = True

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().post(request, *args, **kwargs)

	def get_permission_object(self):
		partner_pk = self.kwargs.get("partner_pk")
		partner = get_object_or_404(Partner, pk=partner_pk)
		return partner

	def get_object(self, queryset=None):
		self.partner = get_object_or_404(Partner, pk=self.kwargs["partner_pk"])
		return get_object_or_404(
			User, pk=self.kwargs["user_pk"], partners__pk=self.kwargs["partner_pk"]
		)

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		name = self.object.get_full_name() or self.object.email or self.object.username
		ctx["partner"] = self.partner
		ctx["title"] = _("Edit user '%s' roles") % name
		return ctx

	def form_valid(self, form):
		change_perm = (
			Partner._meta.app_label
			+ "."
			+ get_permission_codename("change", Partner._meta)
		)
		delete_perm = (
			Partner._meta.app_label
			+ "."
			+ get_permission_codename("delete", Partner._meta)
		)
		cleaned_data = form.cleaned_data
		if cleaned_data["can_edit"]:
			assign_perm(change_perm, self.object, self.partner)
		else:
			remove_perm(change_perm, self.object, self.partner)
		if cleaned_data["can_delete"]:
			assign_perm(delete_perm, self.object, self.partner)
		else:
			remove_perm(delete_perm, self.object, self.partner)
		return super().form_valid(form)

	def get_success_url(self):
		name = self.object.get_full_name() or self.object.email
		messages.success(self.request, _("User '%s' was updated successfully.") % name)
		return reverse("dashboard:partner-list")
