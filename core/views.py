from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
    

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer