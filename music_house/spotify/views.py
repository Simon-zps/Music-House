from django.shortcuts import render
from credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from requests import Request, post
from django.shortcuts import redirect
from . import utils
from api.models import Room
from .models import Token
from .models import Vote
import datetime
import pytz
from django.conf import settings

# First call - passing client ID, scopes and redirect URI, starts the process of authenticating
# user and gets the user's authorization to access data
@api_view(['GET'])
def get_auth(request):
    authorization_scopes = 'streaming app-remote-control user-read-email user-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing'

    url = Request('GET', 'https://accounts.spotify.com/authorize', params={ 
        'scope':authorization_scopes, 
        'response_type':'code', 
        'redirect_uri':REDIRECT_URI,
        'client_id': CLIENT_ID,
        }).prepare().url

    print(url)
    return Response({'url':url})


# Second call - passing authorization code returned by the first call, and secret_key
# to get access and refresh tokens
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
    
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    
    django_timezone = pytz.timezone(settings.TIME_ZONE)
    expires_in = int(response.get('expires_in'))
    expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
    expiration_time_aware = django_timezone.localize(expiration_time)

    error = response.get('error')

    print("Spotify callback, access token:", access_token)
    print("Spotify callback, expires in:", expires_in)
    if not request.session.exists(request.session.session_key):
        request.session.create()

    utils.update_or_create_user_tokens(request.session.session_key, access_token, refresh_token, token_type, expires_in = expiration_time_aware)

    #return redirect('frontend:index')
    return redirect('get_current_song')


@api_view(['GET'])
def is_authenticated(request):
    is_authenticated = utils.is_spotify_authenticated(request.session.session_key)
    return Response({'status': is_authenticated.get('is_authenticated'), 'access_token': is_authenticated.get('access_token')})


@api_view(['GET'])
def get_current_song(request):
    code = request.session.get('code')
    room = Room.objects.filter(code=code).first()

    if room is None:
        return Response({"Error":"Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    host = room.host
    endpoint = "player"
    response = utils.execute_spotify_api_request(host, endpoint)

    if 'error' in response or 'item' not in response:
        return Response({"Error":"No content"}, status=status.HTTP_204_NO_CONTENT)
    
    item = response.get('item')
    
    item = response.get('item')
    duration = item.get('duration_ms')
    progress = response.get('progress_ms')
    album_cover = item.get('album').get('images')[0].get('url') # get prevents potential NoneType errors
    is_playing = response.get('is_playing')
    song_id = item.get('id')
    href = item.get('href')

    artists = item.get('artists')
    artist_string = ', '.join(artist.get('name') for artist in artists)
    votes_submitted = len(Vote.objects.filter(room=room, song_id=song_id))

    song = {
            'title': item.get('name'),
            'artist': artist_string,
            'duration': duration,
            'progress': progress,
            'image_url': album_cover,
            'is_playing': is_playing,
            'votes_required': room.votes_to_skip,
            'votes_submitted':votes_submitted, 
            'id': song_id,
            'song': True,
            'href': href,
        }
    print(href)


    utils.update_room_song(room, song_id)
    return Response(song)


@api_view(['PUT'])
def pause_song(request):
    room = Room.objects.filter(code=request.session.get('code')).first()
    if request.session.session_key == room.host or room.guest_pause_permission:
        utils.pause(room.host)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    return Response({"Message":"Forbidden"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['PUT'])
def play_song(request):
    room = Room.objects.filter(code=request.session.get('code')).first()
    if request.session.session_key == room.host or room.guest_pause_permission:
        utils.play(room.host)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    return Response({"Message":"Forbidden"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def skip_song(request):
    room = Room.objects.filter(code=request.session.get('code')).first()
    votes_required = room.votes_to_skip
    votes = Vote.objects.filter(room=room, song_id=room.current_song)

    if request.session.session_key == room.host or len(votes) >= votes_required:
        # skip song and reset votes
        utils.skip(room.host)
        votes.delete()
    
    else:
        # register new vote 
        vote = Vote(user=request.session.session_key, song_id=room.current_song, room=room )
        vote.save()

    return Response({}, status.HTTP_204_NO_CONTENT)
