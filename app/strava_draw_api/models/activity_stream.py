from django.db import models
from django.contrib.postgres.fields import ArrayField

from strava_draw_api.models import Activity


class ActivityStream(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='activity_streams')
    stream_type = models.CharField()
    data = ArrayField(models.FloatField(), blank=True, null=True) # some streams return integers, so we'll need a method for converting to floats
    original_size = models.IntegerField()

    class Meta:
        unique_together = ('activity', 'stream_type')