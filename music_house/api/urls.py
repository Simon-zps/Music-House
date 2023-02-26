from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getRooms, name='getRooms'),
    path('create-room', views.createRoom, name='createRoom'),
    path('room/<str:code>', views.getRoom, name='getRoom'),
    path('join-room/<str:code>', views.joinRoom, name="joinRoom"),
]