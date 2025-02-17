from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..models import Booking
from ..serializer import BookingSerializer
from ..utils import CustomTokenAuthentication
from rest_framework.permissions import AllowAny


@api_view(["GET", "POST"])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([AllowAny])
def manage_booking(request, fk):
    try:
        booking = Booking.objects.get(pk=fk)
    except Booking.DoesNotExist:
        return Response(f"Thread with ID {fk} can not be found",status=status.HTTP_404_NOT_FOUND)

    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    if request.method == 'GET':
        return Response(serializer.data)
    if request.method == 'POST':
        request.data["user"] = request.user["user_id"]
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([AllowAny])
def booking_detail(request,fk, pk):
    try:
        print("--->", fk, pk)
        booking = Booking.objects.get(pk=pk)
        booking_information = BookingSerializer(booking)
    except Booking.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response(booking_information.data)
    
    if request.method == 'PUT':
        serializer = BookingSerializer(booking, data=booking_information.data|request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        Booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
