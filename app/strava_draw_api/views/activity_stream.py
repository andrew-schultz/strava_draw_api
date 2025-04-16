from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from strava_draw_api.auth import JWTAuthentication
from strava_draw_api.models import ActivityStream, Activity
from strava_draw_api.serializers.activity import ActivitySerializer, ActivityAPISerializer, ActivityFirstAPISerializer, ActivityListSerializer
from strava_draw_api.serializers.activity_stream import ActivityStreamSerializer
from strava_draw_api.services.strava import create_activity_stream

class ActivityStreamAPIView(APIView):
    authentication_classes = (JWTAuthentication,)

    def get(self, request, activity_id):
        user = request.user
        query_params = request.query_params
        stream_types = query_params.get('stream_types')

        try:
            activity = Activity.objects.get(external_id=activity_id, user=user)
        except Activity.DoesNotExist:
            return Response({'error': 'Activity Not Found'}.data)

        streams = activity.activity_streams.all()
        print(streams)
        if not streams:
            streams = create_activity_stream(activity, user.integration, stream_types)

        serializer = ActivityStreamSerializer(streams, many=True)
        return Response(serializer.data)