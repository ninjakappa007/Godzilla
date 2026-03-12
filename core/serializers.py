from django.contrib.auth.models import User
from rest_framework import serializers
from .models import DeviceDetailsModel, DeviceTransactionModel


# Documentation : https://www.django-rest-framework.org/api-guide/serializers/

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    

class DeviceReadSerializer(serializers.ModelSerializer):
    primary_owner = serializers.CharField(read_only=True)
    current_owner = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    
    class Meta:
        model = DeviceDetailsModel
        fields = ['id', 'name', 'primary_owner', 'current_owner', 'serial_number', 'price', 'health_status', 'status']
        
class DeviceWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceDetailsModel
        fields = ['name', 'serial_number', 'price', 'health_status']
        
    def validate_serial_number(self, value):
        if value in DeviceDetailsModel.objects.values_list('serial_number', flat=True):
            raise serializers.ValidationError('Serial number already exists')
        return value