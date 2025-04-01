from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from strava_draw_api.auth import JWTAuthentication
# from strava_draw_api.models import Activity, Integration
from strava_draw_api.serializers.activity import ActivitySerializer, ActivityAPISerializer, ActivityFirstAPISerializer, ActivityListSerializer
from strava_draw_api.services.strava import get_activities
from strava_draw_api.tasks import import_strava_activities


class ActivityAPIView(ListAPIView):
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        queryset = request.user.activities.all().order_by('-start_date')
        try:
            paginated_queryset = self.paginate_queryset(queryset)
            activities = self.get_paginated_response(paginated_queryset)
            activities = dict(activities.data)
            activity_data = ActivitySerializer(paginated_queryset, many=True)

            payload = {
                'activity_data': activity_data.data,
                'next_query': activities['next'],
                'previous_query': activities['previous'],
                'count': activities['count']
            }
            serializer = ActivityAPISerializer(payload)

            return Response(serializer.data)
        except:
            payload = {
                'activity_data': [],
                'next_query': None,
                'previous_query': None,
                'count': 0
            }

        return Response(payload)


class FirstTimeActivityAPIView(APIView):
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        user = request.user
        integration = user.integration

        if integration:
            # get the first batch of activities
            activities = get_activities(integration.account_id, integration.access_token, integration.refresh_token, user, 1, False)

            # kick off the async task to get the rest of the activities
            import_strava_activities.delay(user.id)

            return Response(ActivityFirstAPISerializer({'activities': activities}).data)
        else:
            # an integration wasn't set up correctly, we probably want to handle this error earlier in the flow
            # we don't have the code for strava auth here so we can't retry to set up the integration in this view, it would need to be done in the auth view
            return Response(ActivityFirstAPISerializer({'activities': None}).data)
