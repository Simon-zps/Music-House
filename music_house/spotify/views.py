from django.shortcuts import render
from credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from requests import Request, post
from django.shortcuts import redirect
from . import utils


@api_view(['GET'])
def get_auth(request):
    authorization_scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

    url = Request('GET', 'https://accounts.spotify.com/authorize', params={ 
        'scope':authorization_scopes, 
        'response_type':'code', 
        'redirect_uri':REDIRECT_URI,
        'client_id': CLIENT_ID,
        }).prepare().url

    return Response({'url':url})


@api_view(['GET'])
def spotify_callback(request):
    # Get authorization code and once access is granted, get access and refresh tokens
    code = request.GET.get('code')
    error = request.GET.get('error')

    print(error)

    response = post('https://accounts.spotify.com/api/token',
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }).json()
    
    access_token, refresh_token = response.get('access_token'), response.get('refresh_token')
    expires_in, error = response.get('expires_in'), response.get('error')
    token_type = response.get('token_type')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    utils.update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('frontend:index')


@api_view(['GET'])
def is_authenticated(request):
    is_authenticated = utils.is_spotify_authenticated(request.session.session_key)
    return Response({'status': is_authenticated})

