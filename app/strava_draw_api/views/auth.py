from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from strava_draw_api.auth import JWTAuthentication, AllowAuth, SignatureAuthentication
from strava_draw_api.error import BadRequest
from strava_draw_api.utils import create_api_token
from strava_draw_api.serializers.auth import LoginResponseSerializer, LoginSerializer, SignUpSerializer
from strava_draw_api.services.strava import get_access_token, get_activities
from strava_draw_api.models import Integration
from django.conf import settings
from strava_draw_api.error import AccountExists


class LoginView(APIView):
    authentication_classes = [SignatureAuthentication, ]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email').strip()
        password = serializer.validated_data.get('password').strip()
        user = authenticate(username=email, password=password)
        if user:
            payload = {
                'id': user.id,
                'uuid': user.profile.uuid_encoded
            }
            token = create_api_token(payload)
        else:
            raise NotFound('An account cannot be found for that combination of email and password.\n\nPlease try again or follow the link below to Sign Up.')

        integration = user.integration
        if integration:
            # get a new access token
            strava_token = get_access_token(integration.refresh_token)
            integration.refresh_token = strava_token['refresh_token']
            integration.access_token = strava_token['access_token']
            integration.save()
        resp_serializer = LoginResponseSerializer({'token': token, 'integration': bool(integration)})
        return Response(resp_serializer.data)


class LogOutView(APIView):
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        return Response()


class SignUpView(APIView):
    authentication_classes = (SignatureAuthentication,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email').strip()
        password = serializer.validated_data.get('password').strip()
        password_confirm = serializer.validated_data.get('password_confirm').strip()

        if password == password_confirm:
            try:
                user = User.objects.create_user(email, email=email, password=password)
            except IntegrityError:
                # raise an error that an account already exists
                raise AccountExists("An account for this email already exists. Please follow the link below to Log In.")
        else:
            raise BadRequest("Passwords don't match")

        if user:
            payload = {
                'id': user.id,
                'uuid': user.profile.uuid_encoded
            }
            token = create_api_token(payload)
        else:
            raise NotFound()

        try:
            integration = user.integration
        except Integration.DoesNotExist:
            integration = False

        return Response(LoginResponseSerializer({'token': token, 'integration': bool(integration)}).data)
