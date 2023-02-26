from django.shortcuts import render
from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer
from rest_framework import status
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

    serializer = CreateRoomSerializer(data=request.data)
    print(request.data)

    if serializer.is_valid():
        host = request.session.session_key
        votes_to_skip = serializer.validated_data.get('votes_to_skip')
        guest_pause_permission = serializer.validated_data.get('guest_pause_permission')

        #Checks if room already exists and if so, updates it // filter() is superior to get() as get can cause NameError
        room = Room.objects.filter(host=host).first()

        if room:
            room.votes_to_skip = votes_to_skip
            room.guest_pause_permission = guest_pause_permission
            room.save(update_fields=['votes_to_skip','guest_pause_permission'])
        else:
            room = Room(host=host, votes_to_skip=votes_to_skip, guest_pause_permission=guest_pause_permission)
            room.save()

        return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getRoom(request, code):
    room = Room.objects.filter(code=code).first()
    if room:
        serializer = RoomSerializer(room).data
        serializer['is_host'] = room.host == request.session.session_key
        return Response(serializer)
    
    return Response(serializer)
