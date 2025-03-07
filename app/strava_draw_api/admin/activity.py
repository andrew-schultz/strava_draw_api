from django.contrib import admin
from strava_draw_api.models import Activity, Integration

class ActivityAdmin(admin.ModelAdmin):
    model = Activity
    list_display = (
        'user',
        'activity_type',
        'external_id',
    )

__all__ = [
    'ActivityAdmin'
]