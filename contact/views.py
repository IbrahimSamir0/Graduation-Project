from django.shortcuts import render
from .models import contactModel
from .serializer import contactSerializer
from rest_framework.response import Response
from rest_framework import status 
from .permissions import IsAdmin,AllowAny
from rest_framework.decorators import api_view, permission_classes
#from rest_framework.permissions import IsAuthenticated ,AllowAny
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAdmin])
def contactGET (request,):
    if request.method == 'GET':
        permission_classes = [IsAdmin]
        contacts = contactModel.objects.all()
        serialzer = contactSerializer (contacts , many=True)
        return Response(serialzer.data)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def contactPOST (request):   
    if request.method == 'POST':
        permission_classes=[AllowAny]
        serializer=contactSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status= status.HTTP_201_CREATED)

