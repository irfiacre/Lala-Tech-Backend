from rest_framework import serializers
from .models import Users, Properties, Booking


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    host = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), write_only=True)
    host_details = UsersSerializer(source="host", read_only=True) 
    # host = UsersSerializer()
    class Meta:
        model = Properties
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    property = serializers.SlugRelatedField(queryset=Properties.objects.all(), slug_field="property_id")
    user = serializers.SlugRelatedField(queryset=Users.objects.all(), slug_field="user_id")

    class Meta:
        model = Booking
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["property"] = PropertySerializer(instance.property).data
        representation["user"] = UsersSerializer(instance.user).data
        return representation
