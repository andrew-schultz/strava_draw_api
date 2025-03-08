from rest_framework import serializers
from strava_draw_api.models import Activity
# from .user import UserSerializer


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
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
    

# class StravaActivitySerializer(serializers.Serializer):
    
class ActivityListSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    results = ActivitySerializer(many=True)