import oscar.apps.dashboard.partners.apps as apps


class PartnersDashboardConfig(apps.PartnersDashboardConfig):
	name = "oscar_apps.dashboard.partners"
	default_permissions = []
	permissions_map = {
		"partner-create": (["is-staff"], ["partner.add_partner"]),
	}
