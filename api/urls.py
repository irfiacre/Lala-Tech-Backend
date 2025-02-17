from django.urls import path

from .views import users
from .views import property
from .views import  booking

urlpatterns=[
    path('users/register/', users.register_user_view, name="register_user"),
    path('users/<str:pk>/', users.find_user_view, name="get_user"),
    path('properties/', property.manage_property, name="manage_property"),
    path('properties/<int:pk>/', property.property_detail, name="property_detail"),
    path('bookings/', booking.manage_booking, name="manage_booking"),
    path('bookings/<int:pk>/', booking.booking_detail, name="booking_detail"),
]
