from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import authentication
# from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.renderers import TemplateHTMLRenderer
from django.conf import settings
from strava_draw_api.auth import JWTAuthentication
from strava_draw_api.models import Activity, Integration
# from strava_draw_api.models.spotify_song import build_uri_from_link
# from strava_draw_api.serializers.spotify_song import (
#     SpotifySongSerializer, SpotifySongExtendedSerializer, SpotifyPostSerializer)
# from strava_draw_api.services.spotify import get_track, add_track_to_playlist, build_id_from_uri

class StravaWebhookView(APIView):
    def post(self, request):
        # validate the webhook if they have a mechanism for that
        # probably look up the user, make sure they have an active integration
        # if its a "activity created" event then make an activity
        # if its a "activity deleted" event then look up an activity and delete it if found
        # if its a "user deauthed" event then mark the users integration as revoked at time.now 
        return 