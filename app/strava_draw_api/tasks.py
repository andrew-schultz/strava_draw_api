from celery import shared_task
from django.contrib.auth.models import User
# from strava_draw_api.models import Activity
from strava_draw_api.services.strava import get_all_activities


@shared_task
def import_strava_activities(user_id):
    # make requests to strava with these creds to get a users 
    user = User.objects.filter(id=user_id).select_related('integration').first()
    integration = user.integration
    if integration:
        get_all_activities(integration.account_id, integration.access_token, integration.refresh_token, user, 1, False)
    return True
