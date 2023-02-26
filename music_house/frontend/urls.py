from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('join-room', views.index, name='join-room'),
    path('create-room', views.index, name='create-room'),
    path('room/<str:code>', views.index, name='room')
]
