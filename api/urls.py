from django.urls import path

from api.views import users, property, booking, analytics

urlpatterns=[
    path('users/register/', users.register_user_view, name="register_user"),
    path('users/<str:pk>/', users.find_user_view, name="get_user"),
    path('properties/', property.manage_property, name="manage_property"),
    path('properties/<str:pk>/', property.property_detail, name="property_detail"),
    path('properties/user/<str:userId>/', property.get_host_properties, name="get_host_properties"),
    path('bookings/', booking.manage_booking, name="manage_booking"),
    path('bookings/<str:pk>/', booking.booking_detail, name="booking_detail"),
    path('bookings/user/<str:userId>/', booking.get_user_bookings, name="get_host_bookings"),
    path('analytics/<str:user_id>', analytics.analytics, name="analytics"),
]
