from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DeviceView, DeviceDetailView



router = DefaultRouter()
router.register(r'user', UserViewSet)
# router.register(r'device', DeviceVewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('devices/', DeviceView.as_view(), name='devices'),
    path('device/<int:id>/', DeviceDetailView.as_view(), name='device')
    ]




