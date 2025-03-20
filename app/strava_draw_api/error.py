from rest_framework.exceptions import APIException, ErrorDetail

BAD_REQUEST = 'bad_request'
INVALID_TOKEN = 'invalid_token'
EXPIRED_TOKEN = 'expired_token'
MISSING_TOKEN = 'missing_token'
ACCOUNT_EXISTS = 'account_exists'
# login_failed = 'login_failed'


class BadRequest(APIException):
    status_code = 400
    default_detail = 'Bad request'
    default_code = BAD_REQUEST


class InvalidToken(APIException):
    status_code = 401
    default_detail = 'Invalid token'
    default_code = INVALID_TOKEN


class ExpiredToken(APIException):
    status_code = 401
    default_detail = 'Expired token'
    default_code = EXPIRED_TOKEN


class MissingToken(APIException):
    status_code = 401
    default_detail = 'Missing token'
    default_code = MISSING_TOKEN


class AccountExists(APIException):
    status_code = 400
    default_detail = 'Account already exists'
    default_code = ACCOUNT_EXISTS


# class LoginBadRequest(APIException):
#     status_code = 400
#     default_detail = ''
#     default_code = MISSING_TOKEN
