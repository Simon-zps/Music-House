from django.db import models
import string, random

#Most of your logic should be kept in models - Fat models thin use

#class Host(models.Model):
#   name = models.CharField()

def generate_unique_code():
    length = 6

    while Room.objects.filter(code=code).exists():
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
    
    return code
        

class Room(models.Model):
    code = models.CharField(max_length=8, unique=True)
    #host = models.ForeignKey(Host, models.CASCADE, null=True)  #Transform later into a different Table that can have One To Many relationship
    host = models.CharField(max_length=50, unique=True)
    guest_pause_permission = models.BooleanField(default=False)
    votes_to_skip = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
