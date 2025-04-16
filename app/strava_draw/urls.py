"""
URL configuration for strava_draw project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.http import JsonResponse
# from strava_draw_api.admin import strava_draw_api_site
from strava_draw_api.urls import (
    activity_urlpatterns,
    activity_stream_urlpatterns,
    auth_urlpatterns,
    strava_urlpatterns,
    webhook_urlpatterns,
)


def home(request):
    return JsonResponse({'hello': 'world!'})


urlpatterns = [
    path('', home, name='home'),
    # path('', strava_draw_api_site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('api/v1/activity/', include(activity_urlpatterns)),
    path('api/v1/activity_stream/', include(activity_stream_urlpatterns)),
    path('api/v1/auth/', include(auth_urlpatterns)),
    path('api/v1/strava/', include(strava_urlpatterns)),
    path('api/v1/webhooks/', include(webhook_urlpatterns)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
