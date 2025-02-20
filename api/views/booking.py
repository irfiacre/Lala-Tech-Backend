from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from api.models import Booking, Properties, Users
from api.serializer import BookingSerializer

# {"property": "5fa903c8-0725-4f35-a38d-2d0e2e1dd9fc", "user": "27718c66-e8d9-4e5b-abd3-9ea4bbe09411", "price": 10000, "start_date":"2025-02-18", "end_date":"2025-02-18"}
# { "price": 13000, "start_date":"2024-02-18", "end_date":"2025-05-18" }
@api_view(["GET", "POST"])
def manage_booking(request):
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    if request.method == 'GET':
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        user_instance = get_object_or_404(Users, user_id=request.data.get("user"))
        property_instance = get_object_or_404(Properties, property_id=request.data.get("property"))

        booking_data = request.data.copy()
        booking_data["property"] = property_instance.property_id
        booking_data["user"] = user_instance.user_id 

        serializer = BookingSerializer(data=booking_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PATCH", "DELETE"])
def booking_detail(request, bookingId):
    try:
        booking = Booking.objects.get(pk=bookingId)
        booking_information = BookingSerializer(booking)
    except Booking.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response(booking_information.data)
    
    if request.method == 'PATCH':
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def get_user_bookings(request, userId):
    user_bookings = Booking.objects.filter(host__user_id=userId)
    serializer = BookingSerializer(user_bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def user_property_booking_detail(request, propertyId, userId):
    try:
        if userId and propertyId:
            booking = Booking.objects.filter(property_id=propertyId, user_id=userId).first()
            booking_information = BookingSerializer(booking)
            if not booking_information.data['user']:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(booking_information.data, status=status.HTTP_200_OK)
    except Booking.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)