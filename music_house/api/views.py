from django.shortcuts import render
from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse

@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True).data
    return Response(serializer)


@api_view(['GET', 'POST'])
def get_room(request, code):
    room = Room.objects.filter(code=code).first()
    if room:
        serializer = RoomSerializer(room).data
        serializer['is_host'] = room.host == request.session.session_key
        request.session['code'] = code
        return Response(serializer)
    
    return Response({"Something went wrong":"No such room"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_room(request):
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

        request.session['code'] = room.code
        return Response(RoomSerializer(room).data)


@api_view(['GET'])
def is_user_in_room(request):
    if 'session_key' not in request.session:
        request.session.create()

    data = {
        'code':request.session.get('code') #As request.session['code'] might raise KeyError :(
    }
    return JsonResponse(data)

'''
@api_view(['POST'])
def joinRoom(request, code):
    if 'session_key' not in request.session:
        request.session.create()

    room = Room.objects.filter(code=code).first()
    if room:
        return Response({"message":"You joined a room"})

    return Response({"message":"No such room"}, status=status.HTTP_400_BAD_REQUEST)
'''