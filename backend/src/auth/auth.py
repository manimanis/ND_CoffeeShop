import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'manianis.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'udacity_coffee_shop_api'


# AuthError Exception
class AuthError(Exception):
    """
    AuthError Exception
    A standardized way to communicate auth failure modes
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    """
    Attempt to get the header from the request
        raise an AuthError if no header is present
    Attempt to split bearer and the token
        raise an AuthError if the header is malformed
    :return: the token part of the header
    """
    auth = request.headers.get('Authorization', None)
    if auth is None:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'The authorization header is missing.'
        }, 401)
    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'The authorization header is invalid.'
        }, 401)
    return parts[1]


def check_permissions(permission, payload):
    """
    Check if the user has the permission.
    - Raise an AuthError if permissions are not included in the payload.
    - Raise an AuthError if the requested permission string is not in the
      payload permissions array.
    :param permission: string permission (i.e. 'post:drink')
    :param payload: decoded jwt payload
    :return: True if the user has the permission to do that action
    """
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'Invalid claims.',
            'description': 'Permissions not included in JWT.'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized_access',
            'description': 'The user do not have permission to this resource.'
        }, 403)
    return True


# !!NOTE urlopen has a common certificate error described here:
# https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
def verify_decode_jwt(token):
    """
    Verify and decode the JWT Token. Than returns the payload.
    :param token: a json web token (string)
    :return: The decoded payload if no errors
    """
    # Get the public key from Auth0
    jwks = json.loads(
        urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
        .read()
    )
    # Get the data in the header of the token (JWT=header.payload.signature)
    unv_head = jwt.get_unverified_header(token)
    # Get the RSA key from 'jkws' and compare it with the 'unv_head'
    rsa_key = {}
    if 'kid' not in unv_head:
        raise AuthError({
            'code': 'invalid_token_header',
            'description': 'Token header malformed.'
        }, 401)
    for key in jwks['keys']:
        if key['kid'] == unv_head['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # finally use the key to validate the JWT
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token has expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Invalid claims error.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Invalid header.'
            }, 401)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Invalid header.'
    }, 401)


# '''
# @TODO implement @requires_auth(permission) decorator method
#     @INPUTS
#         permission: string permission (i.e. 'post:drink')
#
# it should use the get_token_auth_header method to get the token
# it should use the verify_decode_jwt method to decode the jwt
# it should use the check_permissions method validate claims and check
# the requested permission
#
# return the decorator which passes the decoded payload to the decorated method
# '''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
                return f(payload, *args, **kwargs)
            except AuthError as error:
                abort(error.status_code)
        return wrapper
    return requires_auth_decorator
