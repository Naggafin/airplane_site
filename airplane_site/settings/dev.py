import os
import sys

from .base import *  # noqa: F403

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

DEBUG = True
SECRET_KEY = "django-insecure--xzwi*2w$a$qe7g+01_fzh%_&i03@8$!t6idzd%o%_acdo*9&m"
ALLOWED_HOSTS = ["*"]


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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# oscar

OSCAR_URL_SCHEMA = "http"


HAYSTACK_CONNECTIONS = {
	"default": {
		"ENGINE": "haystack.backends.simple_backend.SimpleEngine",
	},
}
