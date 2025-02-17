from rest_framework import serializers
from .models import Users, Properties, Booking


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Properties
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True)  # Fetch related properties

    class Meta:
        model = Users
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)
    property = PropertySerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
