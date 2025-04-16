from rest_framework import serializers
from strava_draw_api.models import Activity
# from .user import UserSerializer


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            'id',
            'external_id',
            'activity_type',
            'polyline',
            'duration',
            'distance',
            'avg_watts',
            'avg_speed',
            'work_done',
            'elev_gain',
            'pace',
            'name',
            'start_date',
        )
    pace = serializers.FloatField(required=False, allow_null=True)


# class StravaActivitySerializer(serializers.Serializer):

class ActivityListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    results = ActivitySerializer(many=True)


class ActivityAPISerializer(serializers.Serializer):
    activity_data = ActivitySerializer(many=True, allow_null=True, required=False)
    next_query = serializers.CharField()
    previous_query = serializers.CharField(required=False, allow_null=True)
    count = serializers.IntegerField(required=False)


class ActivityFirstAPISerializer(serializers.Serializer):
    activities = ActivitySerializer(many=True)