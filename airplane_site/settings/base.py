"""
Django settings for airplane_site project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
from oscar.defaults import *  # noqa: F403

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")


# Application definition

INSTALLED_APPS = [
	"airplane_site.apps.AircraftShopConfig",
	# django
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	"django.contrib.sites",
	"django.contrib.flatpages",
	# frontend template
	"pixio",
	# oscar
	"oscar.config.Shop",
	"oscar.apps.analytics.apps.AnalyticsConfig",
	# "oscar.apps.checkout.apps.CheckoutConfig",
	"oscar_apps.checkout.apps.CheckoutConfig",
	"oscar.apps.address.apps.AddressConfig",
	"oscar.apps.shipping.apps.ShippingConfig",
	# "oscar.apps.catalogue.apps.CatalogueConfig",
	"oscar_apps.catalogue.apps.CatalogueConfig",
	"oscar.apps.catalogue.reviews.apps.CatalogueReviewsConfig",
	"oscar.apps.communication.apps.CommunicationConfig",
	# "oscar.apps.partner.apps.PartnerConfig",
	"oscar_apps.partner.apps.PartnerConfig",
	# "oscar.apps.basket.apps.BasketConfig",
	"oscar_apps.basket.apps.BasketConfig",
	"oscar.apps.payment.apps.PaymentConfig",
	"oscar.apps.offer.apps.OfferConfig",
	"oscar.apps.order.apps.OrderConfig",
	# "oscar.apps.customer.apps.CustomerConfig",
	"oscar_apps.customer.apps.CustomerConfig",
	"oscar.apps.search.apps.SearchConfig",
	"oscar.apps.voucher.apps.VoucherConfig",
	# "oscar.apps.wishlists.apps.WishlistsConfig",
	"oscar_apps.wishlists.apps.WishlistsConfig",
	# "oscar.apps.dashboard.apps.DashboardConfig",
	"oscar_apps.dashboard.apps.DashboardConfig",
	"oscar.apps.dashboard.reports.apps.ReportsDashboardConfig",
	"oscar.apps.dashboard.users.apps.UsersDashboardConfig",
	"oscar.apps.dashboard.orders.apps.OrdersDashboardConfig",
	# "oscar.apps.dashboard.catalogue.apps.CatalogueDashboardConfig",
	"oscar_apps.dashboard.catalogue.apps.CatalogueDashboardConfig",
	"oscar.apps.dashboard.offers.apps.OffersDashboardConfig",
	# "oscar.apps.dashboard.partners.apps.PartnersDashboardConfig",
	"oscar_apps.dashboard.partners.apps.PartnersDashboardConfig",
	"oscar.apps.dashboard.pages.apps.PagesDashboardConfig",
	"oscar.apps.dashboard.ranges.apps.RangesDashboardConfig",
	"oscar.apps.dashboard.reviews.apps.ReviewsDashboardConfig",
	"oscar.apps.dashboard.vouchers.apps.VouchersDashboardConfig",
	"oscar.apps.dashboard.communications.apps.CommunicationsDashboardConfig",
	"oscar.apps.dashboard.shipping.apps.ShippingDashboardConfig",
	# allauth
	"allauth_ui",
	"allauth",
	"allauth.account",
	"allauth.socialaccount",
	"allauth.socialaccount.providers.facebook",
	"allauth.socialaccount.providers.google",
	# other 3rd party dependencies
	"taggit",
	"guardian",
	"widget_tweaks",
	"slippers",
	"haystack",
	"treebeard",
	"sorl.thumbnail",
	"django_tables2",
	"template_partials",
	"django_htmx",
	"django_user_agents",
	"django_extensions",
	"view_breadcrumbs",
]

SITE_ID = 1

MIDDLEWARE = [
	"django.middleware.security.SecurityMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"htmx_utils.middleware.HtmxDebugMiddleware",
	"django_htmx.middleware.HtmxMiddleware",
	"htmx_utils.middleware.HtmxRedirectMiddleware",
	"htmx_utils.middleware.HtmxMessagesMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
	"allauth.account.middleware.AccountMiddleware",
	"oscar.apps.basket.middleware.BasketMiddleware",
	"oscar_apps.wishlists.middleware.WishListMiddleware",
	"django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
	"django_user_agents.middleware.UserAgentMiddleware",
]

ROOT_URLCONF = "airplane_site.urls"

TEMPLATES = [
	{
		"BACKEND": "django.template.backends.django.DjangoTemplates",
		"DIRS": [BASE_DIR / "templates"],
		"APP_DIRS": True,
		"OPTIONS": {
			"context_processors": [
				"django.template.context_processors.debug",
				"django.template.context_processors.request",
				"django.contrib.auth.context_processors.auth",
				"django.contrib.messages.context_processors.messages",
				# "oscar_apps.wishlists.context.wishlist",
				"oscar.apps.search.context_processors.search_form",
				"oscar.apps.checkout.context_processors.checkout",
				"oscar.core.context_processors.metadata",
				"htmx_utils.context_processors.htmx_utils_context",
				"airplane_site.context.populate_products",
				"airplane_site.context.site_ui",
			],
			"builtins": [
				"django_extensions.templatetags.misc",
			],
		},
	},
]

WSGI_APPLICATION = "airplane_site.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
	},
]

AUTHENTICATION_BACKENDS = [
	"allauth.account.auth_backends.AuthenticationBackend",
	"guardian.backends.ObjectPermissionBackend",
	"django.contrib.auth.backends.ModelBackend",
]

LOGIN_REDIRECT_URL = "/"


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGES = [
	("en", _("English")),
	("es", _("Spanish")),
]

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_FINDERS = [
	"django.contrib.staticfiles.finders.FileSystemFinder",
	"django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [BASE_DIR / "static"]

STATIC_ROOT = BASE_DIR / "public" / "static"
STATIC_URL = "static/"

MEDIA_ROOT = BASE_DIR / "public" / "media"
MEDIA_URL = "media/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Telegram

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_LOGS_CHAT_ID = os.getenv("TELEGRAM_LOGS_CHAT_ID")


LOGGING = {
	"version": 1,
	"disable_existing_loggers": False,
	"filters": {
		"require_debug_true": {
			"()": "django.utils.log.RequireDebugTrue",
		},
		"require_debug_false": {
			"()": "django.utils.log.RequireDebugFalse",
		},
	},
	"formatters": {
		"django.server": {
			"()": "django.utils.log.ServerFormatter",
			"format": "[{server_time}] {message}",
			"style": "{",
		},
		"verbose": {
			"format": "{asctime} - {name} - {levelname} - {funcName} - {message}",
			"style": "{",
		},
	},
	"handlers": {
		"console": {
			"level": "DEBUG",
			"filters": ["require_debug_true"],
			"class": "logging.StreamHandler",
		},
		"django.server": {
			"level": "INFO",
			"class": "logging.StreamHandler",
			"formatter": "django.server",
		},
		"mail_admins": {
			"level": "ERROR",
			"filters": ["require_debug_false"],
			"class": "django.utils.log.AdminEmailHandler",
		},
		"file": {
			"level": "DEBUG",
			"filters": ["require_debug_false"],
			"class": "logging.FileHandler",
			"filename": BASE_DIR / "django.log",
			"formatter": "verbose",
		},
		"telegram": {
			"level": "ERROR",
			"filters": ["require_debug_false"],
			"class": "telegram_handler.TelegramHandler",
			"token": TELEGRAM_TOKEN,
			"chat_id": TELEGRAM_LOGS_CHAT_ID,
		},
	},
	"loggers": {
		"django": {
			"handlers": ["console", "mail_admins", "file", "telegram"],
			"level": "INFO",
		},
		"django.server": {
			"handlers": ["django.server"],
			"level": "INFO",
			"propagate": False,
		},
		"htmx_utils.middleware": {
			"handlers": ["console"],
			"level": "DEBUG",
		},
	},
}


# site ui settings

SITE_UI_VARS = {
	"num_sidebar_preview_lines": 5,
}


# allauth-ui

ALLAUTH_UI_THEME = "light"


# django-allauth

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
SOCIALACCOUNT_PROVIDERS = {
	"google": {
		"APP": {
			"client_id": os.getenv("ALLAUTH_GOOGLE_CLIENT_ID"),
			"secret": os.getenv("ALLAUTH_GOOGLE_SECRET"),
			"key": os.getenv("ALLAUTH_GOOGLE_KEY"),
		}
	},
	"facebook": {
		"APP": {},
	},
}


# django-oscar

OSCAR_SHOP_NAME = "Aircraft e-commerce site"
OSCAR_SHOP_TAGLINE = ""
OSCAR_INITIAL_ORDER_STATUS = "Pending"
OSCAR_INITIAL_LINE_STATUS = "Pending"
OSCAR_ORDER_STATUS_PIPELINE = {
	"Pending": (
		"Being processed",
		"Cancelled",
	),
	"Being processed": (
		"Processed",
		"Cancelled",
	),
	"Cancelled": (),
}
OSCAR_PRODUCT_MODEL = "catalogue.Product"
OSCAR_ALLOW_ANON_CHECKOUT = True
OSCAR_FROM_EMAIL = "noreply@airvehicleservices.com"
OSCAR_BASKET_COOKIE_OPEN = "aircraft_site_open_basket"
OSCAR_DEFAULT_CURRENCY = "USD"
OSCAR_GOOGLE_ANALYTICS_ID = None


# django-htmx-utils

HTMX_MESSAGES_MIDDLEWARE_TEMPLATE = "pixio/elements/alert.html"
HTMX_MESSAGES_MIDDLEWARE_HTML_ID = "alert-container"


# django-silk

SILKY_PYTHON_PROFILER = False
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_PYTHON_PROFILER_EXTENDED_FILE_NAME = True
SILKY_AUTHENTICATION = True  # User must login
SILKY_AUTHORISATION = True  # User must have permissions
SILKY_META = True
SILKY_INTERCEPT_PERCENT = 100  # log 100% of requests


# django-view-breadcrumbs

BREADCRUMBS_TEMPLATE = "pixio/elements/breadcrumbs.html"
