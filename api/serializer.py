from rest_framework import serializers
from .models import Users, Properties, Booking


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    host = UsersSerializer()
    class Meta:
        model = Properties
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)
    property = PropertySerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
