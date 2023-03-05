from django.shortcuts import render
from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse

@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True).data
    return Response(serializer)


@api_view(['GET'])
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
    if not request.session.exists(request.session.session_key):
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
    
    return Response({"Error:":"Submitted data is invalid"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def is_user_in_room(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()

    data = {'code':''}
    if 'code' in request.session:
        data['code'] = request.session['code']
    return JsonResponse(data)


@api_view(['POST'])
def leave_room(request, code):
    if not request.session.exists(request.session.session_key):
        request.session.create()

    if 'code' in request.session and request.session.get('code') == code:
        del request.session['code']
        request.session.modified = True
        room = Room.objects.filter(code=code).first()
        if room is not None and room.host == request.session.session_key:
            room.delete()
            return Response({"message":"Left room, room deleted"})
        return Response({"message":"Left room"})
    else:
        return Response({"message":"Not in room"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def join_room(request, code):
    if not request.session.exists(request.session.session_key):
        request.session.create()

    room = Room.objects.filter(code=code).first()
    if room:
        request.session['code'] = code
        return Response({"message":"You joined a room"})

    return Response({"message":"No such room"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_room(request):

    # Even though the update_room view is almost identical to create_room, it serves seperate
    # purposes, also it might be helpful to differentiate endpoints when adding more features

    if not request.session.exists(request.session.session_key):
        request.session.create()

    print(request.data)

    serializer = UpdateRoomSerializer(data=request.data)

    if serializer.is_valid():
        user = request.session.session_key
        code = serializer.validated_data.get('code')
        votes_to_skip = serializer.validated_data.get('votes_to_skip')
        guest_pause_permission = serializer.validated_data.get('guest_pause_permission')

        room = Room.objects.filter(code=code).first()

        if room.host != user:
            return Response({"Error":"You're not authorized to change settings!"}, status=status.HTTP_400_BAD_REQUEST)

        if room:
            room.code = code
            room.votes_to_skip = votes_to_skip
            room.guest_pause_permission = guest_pause_permission
            room.save(update_fields=['code', 'votes_to_skip','guest_pause_permission'])
            request.session['code'] = room.code
            return Response(UpdateRoomSerializer(room).data)
        else:
            return Response({"Error:":"Room not found"}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({"Error:":"Submitted data is invalid"}, status=status.HTTP_400_BAD_REQUEST)
