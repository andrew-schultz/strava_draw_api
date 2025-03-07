from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from strava_draw_api.utils import encode_uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    uuid = models.UUIDField(unique=True, default=uuid4)

    @property
    def uuid_encoded(self):
        return encode_uuid(self.uuid)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if not created and hasattr(instance, 'profile'):
        instance.profile.save()
