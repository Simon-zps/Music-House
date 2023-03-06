from .models import Token
from django.utils import timezone
from datetime import timedelta
from credentials import CLIENT_ID, CLIENT_SECRET
from requests import post


def update_or_create_user_tokens(session_id, access_token, refresh_token, token_type, expires_in):
    token = Token.objects.filter(user=session_id).first()
    expires_in = timezone.now() + timedelta(seconds=expires_in)

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
    if token and token.expires_in <= timezone.now():
        refresh_spotify_token()
        return True
    return False


def refresh_spotify_token(token):
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
    expires_in = response.get('expires_in')

    update_or_create_user_tokens(token.user, access_token, token_type, expires_in, token.refresh_token)

