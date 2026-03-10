from django.contrib.auth.models import User 
# or from django.contrib.auth import get_user_model; User = get_user_model()
user = User.objects.create_user(username='john', email='john@example.com', password='secretpassword')
user.save()

class UserService:
    
    @staticmethod
    def create_or_update_user(username, password, email):
        user, created = User.objects.update_or_create(
            username=username,
            password=password,
            email=email 
        )
        return user, created