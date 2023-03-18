from .models import Token
from django.utils import timezone
from datetime import timedelta
from credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, get, put, exceptions
import datetime
import pytz
from django.conf import settings

BASE_URL = 'https://api.spotify.com/v1/me/'

def update_or_create_user_tokens(session_id, access_token, refresh_token, token_type, expires_in):
    token = Token.objects.filter(user=session_id).first()

    if token:
        token.access_token = access_token
        token.refresh_token = refresh_token
        token.expires_in = expires_in
        token.token_type = token_type
        token.save(update_fields=['access_token',
                                   'refresh_token', 'expires_in', 'token_type'])
    else:
        token = Token(user=session_id, access_token=access_token,
            refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        token.save()

    
def is_spotify_authenticated(session_id):
    token = Token.objects.filter(user=session_id).first()
    if not token:
        return {'is_authenticated': False, 'access_token': ''}
        
    expiration_time = token.expires_in
    if expiration_time > timezone.now():
        access_token = token.access_token
        return {'is_authenticated': True, 'access_token': access_token}
        
    refresh_response = refresh_spotify_token(session_id, token)
    if refresh_response == 'error':
        return {'is_authenticated': False, 'access_token': ''}
        
    print("Token refreshed")
    access_token = token.access_token
    return {'is_authenticated': True, 'access_token': access_token}




# Third call - passing refresh_token to generate a new access token
def refresh_spotify_token(session_id, token):
    url = 'https//accounts.spotify.com/api/token'
    response = post(url, data={
        'grant_type': 'refresh_token',
        # Refresh token stays consistent for user throughout its life in DB
        'refresh_token': token.refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')

    django_timezone = pytz.timezone(settings.TIME_ZONE)
    expires_in = int(response.get('expires_in'))
    expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
    expiration_time_aware = django_timezone.localize(expiration_time)

    update_or_create_user_tokens(session_id, access_token, token.refresh_token, token_type, expires_in = expiration_time_aware)


def execute_spotify_api_request(host, endpoint, post_=False, put_=False):
    token = Token.objects.filter(user=host).first()
    data = {}

    if not token:
        return {'error': 'User is not authenticated'}

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token.access_token}'
        }

    try:
        if post_:
            response = post(BASE_URL + endpoint, headers=headers, data=data)
        elif put_:
            response = put(BASE_URL + endpoint, headers=headers, data=data)
        else:
            response = get(BASE_URL + endpoint, headers=headers)
        return response.json()
    
    except exceptions.RequestException as e:
        print(f'Request error: {e}')
        return {'error': 'Problem with request'}

