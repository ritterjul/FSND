from flask import Flask, request, abort
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen


app = Flask(__name__)

AUTH0_DOMAIN = 'fsnd-ritterjul.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'

LOGIN_URL = "https://fsnd-ritterjul.eu.auth0.com/authorize?audience=image&response_type=token&client_id=bhhkPc3PYmijhqa6dECNCSzT9glpebCx&redirect_uri=http://localhost:3000/callback"
# use to obtain access token to perform tests
recent_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZ6MGZQbmtIOEtxdy1ERTZaMTJTUSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtcml0dGVyanVsLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTk3MzZiYTY2YmFkNTBjODU3YTA2YzEiLCJhdWQiOiJpbWFnZSIsImlhdCI6MTU4NzA1MjcxNCwiZXhwIjoxNTg3MDU5OTE0LCJhenAiOiJiaGhrUGMzUFltaWpocWE2ZEVDTkNTelQ5Z2xwZWJDeCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmltYWdlcyIsInBvc3Q6aW1hZ2VzIl19.W8UOeZjiMu1IgTjqHeJY_RP3MYdwWuzsx2q4pDPHCgcokCDmoqJxvRSg941UwJvk2B2lXOJTMXdS8kaPz0RCDAwamhioEhFPGYUVRQwfQ2sNrfDolBwM_rTJpv-UBZ6uhpa7kvwObd7fJquC328dTecxJxYpa_k7pw9mQ3Cvk8ancuSI1_l18nrdTlqhYX_zQfMVF2mqra_BVHRurS6bp_C19smKMkPAPTwPIXwv5zOK84TXFLeyUI1a2Bw1O0uM1s6mrMUv83HOLDYku_MY0rAanJRbByc1bJQqnjWu-uYT4MfU2PJ3vb7Met8PUYGExTUEA6QDvAI6OzrHARtsgg'
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if auth:
        parts = auth.split()
        if parts[0].lower() != 'bearer':
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header must start with "Bearer".'
            }, 401)

        elif len(parts) == 1:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Token not found.'
            }, 401)

        elif len(parts) > 2:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header must be bearer token.'
            }, 401)
        else:
            token = parts[1]
            return token

    else:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)


def verify_decode_jwt(token):
    # get the public key from Autho0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # choose our key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # verify signature
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    else:   
        raise AuthError({
            'code': 'invalid_header',
                    'description': 'Unable to find the appropriate key.'
        }, 400)


def check_permissions(permission, payload):
    if 'permissions' in payload:
        if permission in payload['permissions']:
            return True
        else:
            raise AuthError({
                'code': 'unauthorized',
                'description': 'Permission not found.'
            }, 403)
    else:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Token must include permissions'
        }, 400)
    

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
            except AuthError as err:
                print(err.error['code'] + ': ' + err.error['description'])
                abort(err.status_code)

            try:
                payload = verify_decode_jwt(token)
            except AuthError as err:
                print(err.error['code'] + ': ' + err.error['description'])
                abort(err.status_code)
                
            try:
                check_permissions(permission, payload)
            except AuthError as err:
                print(err.error['code'] + ': ' + err.error['description'])
                abort(err.status_code)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator



@app.route('/images')
@requires_auth('get:images')
def headers(payload):
    return 'Access Granted'

