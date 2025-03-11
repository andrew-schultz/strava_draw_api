from django.contrib import admin
from strava_draw_api.models import Integration


class IntegrationAdmin(admin.ModelAdmin):
    model = Integration
    list_display = (
        'user',
        'account_id',
    )


__all__ = [
    'IntegrationAdmin'
]
