import os

from .base import *  # noqa: F403

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

DEBUG = False
SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

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


# Cache
# https://docs.djangoproject.com/en/5.0/topics/cache

CACHES = {
	"default": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": os.environ.get("REDIS_URL"),
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
			"PARSER_CLASS": "redis.connection._HiredisParser",
		},
	},
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"


HAYSTACK_CONNECTIONS = {
	"default": {
		"ENGINE": "haystack.backends.solr_backend.SolrEngine",
		"URL": os.getenv("SOLR_URL"),
		"INCLUDE_SPELLING": True,
	},
}
