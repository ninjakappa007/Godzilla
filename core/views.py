from django.contrib.auth.models import User
from core.serializers import UserSerializer, DeviceReadSerializer, DeviceWriteSerializer, TransactionSerializer
from rest_framework.viewsets import ModelViewSet
from core.models import DeviceDetailsModel, DeviceTransactionModel, DeviceStatus
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from django.core.cache import cache
from core.constants import *
from django.db import transaction


logger = logging.getLogger(__name__)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class DeviceView(APIView):
    def get(self, request):
        device_data = cache.get(AVAILABLE_DEVICES)
        
        if device_data is None:
            devices = DeviceDetailsModel.objects.exclude(is_deleted=True)
            device_data = DeviceReadSerializer(devices, many=True).data
            cache.set(AVAILABLE_DEVICES, device_data, timeout=120)
            
        return Response(device_data, status=status.HTTP_200_OK)

    
    def post(self, request):
        serialized_data = DeviceWriteSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save(primary_owner = request.user)
            cache.delete(AVAILABLE_DEVICES)
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        else:
            error = {'error' : serialized_data.errors}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
  
class DeviceDetailView(APIView):
    def get(self, request, id):
        try:
            device = DeviceDetailsModel.objects.get(id=id)
            serialized_data = DeviceReadSerializer(device)
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        except DeviceDetailsModel.DoesNotExist:
            error = {'error' : 'device not found'}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, id):
        try:
            device = DeviceDetailsModel.objects.get(id=id)
            serialized_data = DeviceWriteSerializer(device, data=request.data, partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                cache.delete(AVAILABLE_DEVICES)
                return Response(serialized_data.data, status=status.HTTP_200_OK)
            else:
                error = {'error' : serialized_data.errors}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except DeviceDetailsModel.DoesNotExist:
            error = {'error' : 'device not found'}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, id):
        try:
            device = DeviceDetailsModel.objects.get(id=id)
            device.is_deleted = True
            device.save()
            cache.delete(AVAILABLE_DEVICES)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except DeviceDetailsModel.DoesNotExist:
            error = {'error' : 'device not found'}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        

class DeviceTransactionView(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                device = DeviceDetailsModel.objects.select_for_update().get(id=request.data.get('device'))
                if device.status != DeviceStatus.AVAILABLE:
                    return Response({'error' : 'device is not available for loan'}, status=status.HTTP_400_BAD_REQUEST)

                serialized_data = TransactionSerializer(data = request.data)
                if serialized_data.is_valid():
                    serialized_data.save(requester=request.user)
                    device.status = DeviceStatus.LOANED
                    device.save()
                    cache.delete(AVAILABLE_DEVICES)
                    return Response(serialized_data.data, status=status.HTTP_201_CREATED)
                else:
                    error = {'error' : serialized_data.errors}
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
        
        except DeviceDetailsModel.DoesNotExist:
            error = {'error' : 'device not found'}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
