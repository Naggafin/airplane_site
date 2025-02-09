import logging
import os
import sys

from .base import *  # noqa: F403

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

DEBUG = True
SECRET_KEY = "django-insecure--xzwi*2w$a$qe7g+01_fzh%_&i03@8$!t6idzd%o%_acdo*9&m"
ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ["*", "127.0.0.1", "localhost"]

INSTALLED_APPS.append("django_fastdev")  # noqa: F405


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if "test" not in sys.argv and os.environ.get("DB_HOST"):
	DATABASES = {
		"default": {
			"ENGINE": "django.db.backends.postgresql",
			"NAME": os.environ.get("DB_NAME"),
			"USER": os.environ.get("DB_USER"),
			"PASSWORD": os.environ.get("DB_PASSWORD"),
			"HOST": os.environ.get("DB_HOST"),
			"PORT": os.environ.get("DB_PORT"),
		},
	}
elif "test" in sys.argv and os.environ.get("TEST_DB_HOST"):
	DATABASES = {
		"default": {
			"ENGINE": "django.db.backends.postgresql",
			"NAME": os.environ.get("TEST_DB_NAME"),
			"USER": os.environ.get("TEST_DB_USER"),
			"PASSWORD": os.environ.get("TEST_DB_PASSWORD"),
			"HOST": os.environ.get("TEST_DB_HOST"),
			"PORT": os.environ.get("TEST_DB_PORT"),
		},
	}
else:
	DATABASES = {
		"default": {
			"ENGINE": "django.db.backends.sqlite3",
			"NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
		},
	}


# Cache
# https://docs.djangoproject.com/en/5.0/topics/cache

CACHES = {
	"default": {
		"BACKEND": "django.core.cache.backends.locmem.LocMemCache",
	},
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# oscar
OSCAR_URL_SCHEMA = "http"


HAYSTACK_CONNECTIONS = {
	"default": {
		"ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
		"PATH": BASE_DIR / "whoosh_index",  # noqa: F405
	},
}


# Debug Toolbar settings
INSTALLED_APPS.append("debug_toolbar")  # noqa: F405
try:
	index = MIDDLEWARE.index("django.contrib.sessions.middleware.SessionMiddleware") + 1  # noqa: F405
except ValueError:
	index = 0
MIDDLEWARE.insert(index, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405
DEBUG_TOOLBAR_CONFIG = {
	"SHOW_TOOLBAR_CALLBACK": "airplane_site.middleware.show_toolbar_superuser"
}


# nplusone
INSTALLED_APPS.append("nplusone.ext.django")  # noqa: F405
MIDDLEWARE.insert(0, "nplusone.ext.django.NPlusOneMiddleware")  # noqa: F405
NPLUSONE_LOGGER = logging.getLogger("nplusone")
NPLUSONE_LOG_LEVEL = logging.WARN
NPLUSONE_RAISE = False
LOGGING["loggers"]["nplusone"] = {  # noqa: F405
	"handlers": ["console"],
	"level": logging.WARN,
}


# django-allauth
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "HTTP"
