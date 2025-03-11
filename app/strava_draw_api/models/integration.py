from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from strava_draw_api.utils import encode_uuid


class Integration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='integration')
    uuid = models.UUIDField(unique=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    revoked_at = models.DateTimeField(
        help_text='When a user revoked access to the 3rd party integration',
        blank=True,
        null=True
    )
    scope = models.CharField(max_length=255, blank=True, null=True, help_text='comma delimited string, eg: "activity:read,activity:write"')
    refresh_token = models.CharField(help_text='token to exchange for an access_token')
    access_token = models.CharField(help_text='short-lived token used to make API calls on behalf of the user')
    expires_at = models.PositiveIntegerField(help_text='the number of seconds since the epoch when the access_token will expire')
    auto_import = models.BooleanField(default=False)
    auto_export = models.BooleanField(default=False)
    initial_sync = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    account_id = models.PositiveIntegerField(blank=True, null=True)

    @property
    def uuid_encoded(self):
        return encode_uuid(self.uuid)
