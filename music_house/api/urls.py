from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_rooms, name='getRooms'),
    path('create-room', views.create_room, name='createRoom'),
    path('room/<str:code>', views.get_room, name='getRoom'),
    path('user-in-room', views.is_user_in_room, name="isUserInRoom"),
]