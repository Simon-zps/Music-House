from django.urls import path
from . import views

urlpatterns = [
    path('get-auth', views.get_auth, name="get-authorization"),
    path('redirect-auth', views.spotify_callback, name="spotify_callback"),
    path('is-auth', views.is_authenticated, name="is_authenticated"),
]
