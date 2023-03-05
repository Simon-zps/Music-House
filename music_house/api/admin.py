from django.contrib import admin
from .models import Room
from spotify.models import Token

admin.site.register(Room)
admin.site.register(Token)
# Register your models here.
