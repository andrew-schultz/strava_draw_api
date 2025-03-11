from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.urls import path

from .auth import GroupAdmin, UserAdmin
from .activity import ActivityAdmin
from .integration import IntegrationAdmin

from strava_draw_api.models import Activity, Integration


class BudBandAdminSite(AdminSite):
    site_header = 'Strava Draw Admin'
    index_title = 'Dashboard'
    site_url = None


strava_draw_api_site = BudBandAdminSite()

strava_draw_api_site.register(Activity, ActivityAdmin)
strava_draw_api_site.register(Integration, IntegrationAdmin)

# AUTHENTICATION AND AUTHORIZATION
strava_draw_api_site.register(Group, GroupAdmin)
strava_draw_api_site.register(User, UserAdmin)
