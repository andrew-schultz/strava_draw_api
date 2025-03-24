from rest_framework.views import APIView
from rest_framework.response import Response
from strava_draw_api.auth import JWTAuthentication, AllowAuth, SignatureAuthentication
from strava_draw_api.services.strava import get_authorization, get_access_token, get_all_activities
from strava_draw_api.serializers.auth import AuthResponseSerializer


class AuthAPIView(APIView):
    authentication_classes = [JWTAuthentication, SignatureAuthentication, ]

    def get(self, request):
        return Response()

    def post(self, request):
        data = request.data
        code = data.get('code')
        scope = data.get('scope')
        user = request.user
        integration = get_authorization(code, user, scope)

        if integration:
            activities = get_all_activities(integration.account_id, integration.access_token, integration.refresh_token, user, 1, False)
            return Response(AuthResponseSerializer({'success': True, 'activities': activities[:100]}).data)
        else:
            # there was an error authorizing the code (or something else)
            # return error
            return Response(AuthResponseSerializer({'success': False, 'activities': None}).data)
        # we could get the activities and return those?
        # sure, cause we don't want to return the acces token obvi, and that saves us from making another request immediately to get those activities


class TokenAPIView(APIView):
    authentication_classes = (AllowAuth,)

    def post(self, request):
        # maybe this is like the user submitting a refresh token to get a fresh jwt for BE requests?
        return Response()
