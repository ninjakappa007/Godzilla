from django.contrib.auth.models import User
from .serializers import UserSerializer, DeviceReadSerializer, DeviceWriteSerializer
from rest_framework.viewsets import ModelViewSet
from .models import DeviceDetailsModel, DeviceTransactionModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class DeviceView(APIView):
    def get(self, request):
        devices = DeviceDetailsModel.objects.exclude(is_deleted=True)
        serialized_data = DeviceReadSerializer(devices, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serialized_data = DeviceWriteSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save(primary_owner = request.user)
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
            return Response(status=status.HTTP_204_NO_CONTENT)
        except DeviceDetailsModel.DoesNotExist:
            error = {'error' : 'device not found'}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        
"""
TODO : redis caching
transaction views
select_for_update()
cache invalidation after post and patch and delete
"""
