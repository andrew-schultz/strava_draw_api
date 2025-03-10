from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from strava_draw_api.auth import JWTAuthentication
# from strava_draw_api.models import Activity, Integration
from strava_draw_api.serializers.activity import ActivitySerializer, ActivityAPISerializer, ActivityListSerializer
from strava_draw_api.services.strava import get_activities


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