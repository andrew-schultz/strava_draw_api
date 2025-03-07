import base64
import os
import time
import uuid
from binascii import hexlify

import jwt
from django.contrib.auth.models import AnonymousUser, User
from django.db.models import Q
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
import hashlib
import hmac
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.encoding import force_bytes
from strava_draw_api.error import ExpiredToken, InvalidToken, MissingToken


def generate_signature(request: HttpRequest, secret_key: str) -> str:
    """Generates a signature for the request."""
    # message = force_bytes(f"{request.body.decode()}-{time.time()}")
    message = force_bytes(f"{request.body.decode()}")
    secret = force_bytes(secret_key)
    signature = hmac.new(secret, message, hashlib.sha256).digest()
    return base64.b64encode(signature).decode()


def verify_signature(request: HttpRequest, secret_key: str, received_signature: str) -> bool:
    """Verifies the signature of the request."""
    generated_signature = generate_signature(request, secret_key)
    return hmac.compare_digest(generated_signature, received_signature)


class SignatureAuthentication(BaseAuthentication):
    model = None

    def get_model(self):
        return User
    
    def authenticate(self, request):
        key = settings.SIG_KEY
        signature = request.headers.get('Authorization')
        if verify_signature(request, key, signature):
            return (AnonymousUser, None)
        else:
            return (None, None)


class JWTAuthentication(BaseAuthentication):
    model = None

    def get_model(self):
        return User

    def authenticate_header(self, request):
        return 'Bearer'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth:
            raise MissingToken("Auth token is a required field")

        if len(auth) != 2:
            raise InvalidToken("Invalid auth header")

        bearer, token = auth
        if bearer != b'Bearer':
            raise InvalidToken("Bearer is a required field")

        # get jwt secret from env var
        jwt_secret = None
        try:
            jwt_secret = os.environ['JWT_SECRET']
        except KeyError:
            raise InvalidToken("JWT_SECRET not defined")

        # decode the token
        try:
            print('token', token)
            decode_token = token.decode()
            print('decode token', decode_token)
            # payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
            payload = jwt.decode(decode_token, settings.JWT_SECRET, algorithms=['HS256'])
            
            print('payload', payload)
        except jwt.ExpiredSignatureError:
            raise ExpiredToken("Signature expired")
        except jwt.exceptions.DecodeError:
            print('whyyyy')
            raise InvalidToken("Decode error")
        except jwt.InvalidTokenError:
            raise InvalidToken("Invalid token")

        # user should always be encoded in token
        user = payload.get('user', None)
        if user is None:
            raise InvalidToken("Invalid payload")

        # get user uuid and decode
        uuid_value = user.get('uuid', None)

        try:
            uuid.UUID(uuid_value)
        except ValueError:
            uuid_value = hexlify(base64.urlsafe_b64decode(uuid_value + '==')).decode()

        # make sure user is valid
        user = None
        try:
            user = User.objects.get(profile__uuid=uuid_value)
        except User.DoesNotExist:
            raise InvalidToken("Invalid user associated with jwt")

        return (user, token)


class AppUser(AnonymousUser):
    """ Django authentication requires a returned user. SignatureAuthentication will return an
    instance of this class"""
    is_authenticated = False

    def __init__(self, is_authenticated=False):
        self.is_authenticated = is_authenticated

    def get_username():
        return 'app_user'


class AllowAuth(BaseAuthentication):
    # model = None
    def authenticate(self, request):
        return (AppUser, None)
    

