from django.urls import path
from . import views

urlpatterns = [
    path('get-auth', views.get_auth, name="get-auth"),
]