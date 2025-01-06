"""
URL configuration for airplane_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from allauth.account.decorators import secure_admin_login
from django.apps import apps
from django.conf import settings
from django.conf.urls import handler400, handler403, handler404, handler500
from django.contrib import admin
from django.urls import include, path

admin.autodiscover()
admin.site.login = secure_admin_login(admin.site.login)

urlpatterns = [
	path("i18n/", include("django.conf.urls.i18n")),
	path("admin/", admin.site.urls),
	path("accounts/", include("allauth.urls")),
	path("", include("pixio.urls")),
	path("", include(apps.get_app_config("airplane_site").urls[0])),
]

if not settings.DEBUG:
	urlpatterns.append(path("silk/", include("silk.urls", namespace="silk")))

if settings.DEBUG:
	import debug_toolbar
	from django.conf.urls.static import static
	from django.contrib.staticfiles.urls import staticfiles_urlpatterns

	# Serve static and media files from development server
	urlpatterns = staticfiles_urlpatterns() + urlpatterns
	urlpatterns = (
		static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
	)
	urlpatterns = [
		path("__debug__/", include(debug_toolbar.urls)),
		path("400/", handler400, kwargs={"exception": Exception("Bad request")}),
		path("403/", handler403, kwargs={"exception": Exception("Forbidden")}),
		path("404/", handler404, kwargs={"exception": Exception("Page not found")}),
		path("500/", handler500, kwargs={"exception": Exception("Server error")}),
	] + urlpatterns
