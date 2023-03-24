from django.db import models
from api.models import Room

class Token(models.Model):
    # by default blank and null are false!
    user = models.CharField(max_length=50, unique=True)
    access_token = models.CharField(max_length=150)
    refresh_token = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    token_type = models.CharField(max_length=50)
    expires_in = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)

    # auto_now assigns new value every time object is saved
    # auto_now_add assigns new value just when we create object for the first time

    class Meta:
        unique_together = (('user', 'access_token'),('user','refresh_token'))

    def __str__(self):
        return f'User: {self.user} access token: {self.access_token}, refresh token: {self.refresh_token}'


class Vote(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    song_id =  models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)