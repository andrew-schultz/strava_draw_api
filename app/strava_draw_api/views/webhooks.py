from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from strava_draw_api.models import Activity
from strava_draw_api.serializers.strava import StravaRequestSerializer
from strava_draw_api.services.strava import create_strava_activity, update_strava_activity

VERIFY_TOKEN = 'stravadrawapiverifytoken1'


class StravaWebhookView(APIView):

    def get(self, request):
        query_params = request.query_params
        mode = query_params['hub.mode']
        token = query_params['hub.verify_token']
        challenge = query_params['hub.challenge']

        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('webhook verified')
                return Response({"hub.challenge":challenge})
            else:
                raise PermissionDenied

        return Response()

    def post(self, request):
        serializer = StravaRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data
        action = valid_data['aspect_type']
        external_id = valid_data['object_id']
        athlete_id = valid_data['owner_id']
        try:
            user = User.objects.get(integration__account_id=athlete_id)
        except User.DoesNotExist:
            return Response()
        print('webhook update', action, external_id, athlete_id)
        if action == 'create':
            activity = create_strava_activity(external_id, user.integration.access_token, user)
        elif action == 'update':
            try:
                activity = Activity.objects.get(external_id=external_id)
                activity = update_strava_activity(external_id, user.integration.access_token, user, activity)
                print('updated_activity name', activity.name)
            except Activity.DoesNotExist:
                activity = create_strava_activity(external_id, user.integration.access_token, user)
        elif action == 'delete':
            try:
                activity = Activity.objects.get(external_id=external_id)
                activity.delete()
            except Activity.DoesNotExist:
                # it's not in the database, do don't need to delete
                pass

        return Response()
