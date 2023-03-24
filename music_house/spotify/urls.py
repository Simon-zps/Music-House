from django.urls import path, include
from . import views

urlpatterns = [
    path('get-auth', views.get_auth, name="get_authorization"),
    path('redirect-auth', views.spotify_callback, name="spotify_callback"),
    path('is-auth', views.is_authenticated, name="is_authenticated"),
    path('current-song', views.get_current_song, name="get_current_song"),
    path('pause', views.pause_song, name='pause_song'),
    path('play', views.play_song, name='play_song'),
    path('skip', views.skip_song, name='skip_song'),
    path('', include(('frontend.urls', 'frontend'), namespace='frontend')),
]
