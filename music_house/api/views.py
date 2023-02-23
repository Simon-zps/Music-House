from django.shortcuts import render
from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True).data
    return Response(serializer)


@api_view(['POST'])
def createRoom(request):
    if 'session_key' not in request.session:
        request.session.create()
