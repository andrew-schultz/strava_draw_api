import base64
import jwt
import random
import uuid as uuid_lib
from binascii import hexlify
from datetime import timedelta
from django.conf import settings
from django.utils import timezone


def create_jwt(payload):
    """JSON Web Token"""
    payload.update(
        {'exp': timezone.now() + timedelta(days=100.0)})
    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm='HS256'
    )
    print('payload in here', payload)
    print('token', token)
    try:
        token.decode()
    except:
        pass
    # return token.decode()
    return token

def create_api_token(info):
    return create_jwt({'user': info or None})

def get_rand(length=24):
    """Cryptographically sound random numbers from the OS"""
    return base64.urlsafe_b64encode(os.urandom(length)).decode()

def encode_uuid(uuid):
    """Encode a UUID into a 22-character string"""
    if type(uuid) is str:
        uuid = uuid_lib.UUID(uuid)
    return base64.urlsafe_b64encode(uuid.bytes).decode()[:22]

def decode_uuid(encoded):
    """Decode a UUID from a 22-character string"""
    if len(encoded) != 22:
        return None
    return hexlify(base64.urlsafe_b64decode(encoded + '==')).decode()


# def create_session(user):
#     return Session.objects.create(
#         session_id=get_rand(),
#         user_id=user.id,
#         expires=timezone.now() + timedelta(days=settings.USER_SESSION_EXPIRY_DAYS)
#     )
