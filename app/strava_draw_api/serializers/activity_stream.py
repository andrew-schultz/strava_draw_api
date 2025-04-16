from rest_framework import serializers
from strava_draw_api.models import ActivityStream


class ActivityStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityStream
        fields = (
            'activity_id',
            'stream_type',
            'data',
            'original_size',
        )
