from django.shortcuts import render
from rest_framework import generics
from .models import Room
from .serializers import RoomSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True).data
    return Response(serializer)
