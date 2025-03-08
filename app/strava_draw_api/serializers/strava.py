from rest_framework import serializers



class StravaRequestUpdatesSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    type = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    private = serializers.BooleanField(required=False)
    authorized = serializers.BooleanField(required=False)


class StravaRequestSerializer(serializers.Serializer):
    object_type = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    object_id = serializers.IntegerField()
    aspect_type = serializers.CharField()
    updates = StravaRequestUpdatesSerializer()
    owner_id = serializers.IntegerField()
    subscription_id = serializers.IntegerField()
    event_time = serializers.IntegerField()
