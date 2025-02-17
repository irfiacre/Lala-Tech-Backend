from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..models import Properties
from ..serializer import PropertySerializer
from ..utils import CustomTokenAuthentication
from rest_framework.permissions import AllowAny

#{"title": "Test property", "description":"To test"}

@api_view(["GET", "POST"])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([AllowAny])
def manage_property(request):
    properties = Properties.objects.all()
    serializer = PropertySerializer(properties, many=True)
    if request.method == 'GET':
        return Response(serializer.data)
    if request.method == 'POST':
        request.data["user"] = request.user["user_id"]
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([AllowAny])
def property_detail(request, pk):
    try:
        property = Properties.objects.get(pk=pk)
        property_information = PropertySerializer(property)
    except Properties.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response(property_information.data)
    
    if request.method == 'PUT':
        serializer = PropertySerializer(property, data=property_information.data|request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        Properties.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
