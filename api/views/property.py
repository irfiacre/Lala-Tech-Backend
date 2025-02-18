from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Properties
from api.serializer import PropertySerializer

# { "title": "Test Property", "description": "Very Good property", "host": "27718c66-e8d9-4e5b-abd3-9ea4bbe09411", "price": 10000, "rooms": 5, "province": "Kigali", "district": "Kicukiro", "sector":"Kanombe", "furnished": true }
# { "title": "Kigali Property", "price": 15000, "furnished": false }
@api_view(["GET", "POST"])
def manage_property(request):
    properties = Properties.objects.all()
    serializer = PropertySerializer(properties, many=True)
    if request.method == 'GET':
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PATCH", "DELETE"])
def property_detail(request, pk):
    try:
        property = Properties.objects.get(pk=pk)
        property_information = PropertySerializer(property)
    except Properties.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response(property_information.data)
    
    if request.method == 'PATCH':
        serializer = PropertySerializer(property, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        property.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def get_host_properties(request, userId):
    user_properties = Properties.objects.filter(host__user_id=userId)
    serializer = PropertySerializer(user_properties, many=True)
    if request.method == 'GET':
        return Response(serializer.data, status=status.HTTP_200_OK)
