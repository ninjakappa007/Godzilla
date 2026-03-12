from django.db import models
from django.conf import settings


class DeviceHealthStatus(models.TextChoices):
    HEALTHY = 'HEALTHY', 'HEALTHY'
    NOT_WORKING = 'NOT_WORKING', 'NOT_WORKING'
    LOST = 'LOST', 'LOST'
    SCRAP = 'SCRAP', 'SCRAP'
    
class DeviceTransactionTypes(models.TextChoices):
    LOAN = 'LOAN', 'LOAN'
    TRANSFER = 'TRANSFER', 'TRANSFER'
    
class TransactionStatusTypes(models.TextChoices):
    PENDING = 'PENDING', 'PENDING'
    APPROVED = 'APPROVED', 'APPROVED'
    REJECTED = 'REJECTED', 'REJECTED'
    CANCELLED = 'CANCELLED', 'CANCELLED'

class DeviceStatus(models.TextChoices):
    AVAILABLE = 'AVAILABLE', 'AVAILABLE'
    LOANED = 'LOANED', 'LOANED'
    MAINTENANCE = 'MAINTENANCE', 'MAINTENANCE'


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
       
class DeviceDetailsModel(BaseModel):
    name = models.CharField(max_length=255, db_index=True)
    primary_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='owned_devices')
    current_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='currently_held_devices', null=True, blank=True)
    serial_number = models.CharField(max_length=255, db_index=True, unique=True)
    is_deleted = models.BooleanField(default=False)
    price = models.IntegerField(null=True, blank=True) # default value of null and blank is False
    health_status = models.CharField(max_length=255, choices=DeviceHealthStatus, default=DeviceHealthStatus.HEALTHY)
    transfer_count = models.IntegerField(default=0)
    status = models.CharField(max_length=255, choices=DeviceStatus, default=DeviceStatus.AVAILABLE)
    
    class Meta:
        db_table = 'device_detail'
        indexes = [
            models.Index(fields=['primary_owner', 'created_at'], name='user_created_index')
        ]

class DeviceTransactionModel(BaseModel):
    device = models.ForeignKey(DeviceDetailsModel, on_delete=models.PROTECT)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    type = models.CharField(max_length=255, choices=DeviceTransactionTypes, db_index=True)
    status = models.CharField(max_length=255, choices=TransactionStatusTypes)
    
    class Meta:
        db_table = 'device_transaction'
        indexes = [
            models.Index(fields=['status', 'created_at'], name='status_created_index')
        ]

    
    
