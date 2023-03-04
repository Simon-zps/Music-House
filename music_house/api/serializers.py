from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Room, generate_unique_code

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('__all__')

class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['guest_pause_permission','votes_to_skip']

class UpdateRoomSerializer(serializers.ModelSerializer):

    code = serializers.CharField(max_length=8, validators=[UniqueValidator(queryset=Room.objects.all())], default=generate_unique_code)

    class Meta:
        model = Room
        fields = ['code', 'guest_pause_permission','votes_to_skip']
