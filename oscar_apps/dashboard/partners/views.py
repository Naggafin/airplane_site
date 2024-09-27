from django.contrib.auth import get_permission_codename
from django.core.exceptions import PermissionDenied
from guardian.mixins import PermissionListMixin, PermissionRequiredMixin
from guardian.utils import get_40x_or_None
from oscar.apps.dashboard.partners.views import (
	PartnerCreateView as OscarPartnerCreateView,
	PartnerDeleteView as OscarPartnerDeleteView,
	PartnerListView as OscarPartnerListView,
	PartnerManageView as OscarPartnerManageView,
	PartnerUserCreateView as OscarPartnerUserCreateView,
	PartnerUserLinkView as OscarPartnerUserLinkView,
	PartnerUserSelectView as OscarPartnerUserSelectView,
	PartnerUserUnlinkView as OscarPartnerUserUnlinkView,
	PartnerUserUpdateView as OscarPartnerUserUpdateView,
)
from oscar.apps.partner.models import Partner
from oscar.core.compat import get_user_model

User = get_user_model()


class PartnerListView(PermissionListMixin, OscarPartnerListView):
	permission_required = (
		Partner._meta.app_label + "." + get_permission_codename("view", Partner._meta)
	)


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


class PartnerDeleteView(PermissionRequiredMixin, OscarPartnerDeleteView):
	permission_required = (
		Partner._meta.app_label + "." + get_permission_codename("delete", Partner._meta)
	)
	return_403 = True


class PartnerUserCreateView(PermissionRequiredMixin, OscarPartnerUserCreateView):
	permission_required = {
		"partner": Partner._meta.app_label
		+ "."
		+ get_permission_codename("change", Partner._meta),
		"user": User._meta.app_label + "." + get_permission_codename("add", User._meta),
	}
	return_403 = True

	def check_permissions(self, request):
		# check if can manage partner first
		forbidden = get_40x_or_None(
			request,
			perms=self.permission_required["partner"],
			obj=self.partner,
			login_url=self.login_url,
			redirect_field_name=self.redirect_field_name,
			return_403=self.return_403,
			return_404=self.return_404,
			any_perm=self.any_perm,
		)
		# now check if can add users
		if not forbidden:
			forbidden = get_40x_or_None(
				request,
				perms=self.permission_required["user"],
				login_url=self.login_url,
				redirect_field_name=self.redirect_field_name,
				return_403=self.return_403,
				return_404=self.return_404,
				accept_global_perms=True,
				any_perm=self.any_perm,
			)

		if forbidden:
			self.on_permission_check_fail(request, forbidden, obj=self.partner)
		if forbidden and self.raise_exception:
			raise PermissionDenied()
		return forbidden


class PartnerUserSelectView(OscarPartnerUserSelectView):
	pass  # TODO


class PartnerUserLinkView(OscarPartnerUserLinkView):
	pass  # TODO


class PartnerUserUnlinkView(OscarPartnerUserUnlinkView):
	pass  # TODO


class PartnerUserUpdateView(OscarPartnerUserUpdateView):
	pass  # TODO
