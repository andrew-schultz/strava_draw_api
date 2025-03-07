from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# from strava_draw_api.models import Integration
from strava_draw_api.utils import encode_uuid

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    integration = models.ForeignKey('Integration', on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, default=uuid4)
    external_id = models.PositiveBigIntegerField()
    activity_type = models.CharField()
    duration = models.PositiveIntegerField()
    distance = models.FloatField()
    avg_watts = models.FloatField()
    avg_speed = models.FloatField()
    work_done = models.FloatField()
    elev_gain = models.FloatField()
    polyline = models.CharField(help_text='comes from an activities map.summary_polyline attribute')
    name = models.CharField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)

    @property
    def pace(self):
        self.duration / self.distance

    @property
    def uuid_encoded(self):
        return encode_uuid(self.uuid)