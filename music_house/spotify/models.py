from django.db import models

class Token(models.Model):
    # by default blank and null are false !
    user = models.CharField(max_length=50, unique=True)
    access_token = models.CharField(max_length=150)
    refresh_token = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    token_type = models.CharField(max_length=50)
    expires_in = models.DateTimeField()

    def __str__(self):
        return self.access_token
