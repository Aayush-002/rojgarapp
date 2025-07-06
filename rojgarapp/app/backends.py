from django.contrib.auth.backends import ModelBackend
from .models import CustomUser


class PhoneNumberBackend(ModelBackend):
    """
    Custom authentication backend that allows users to login with phone number and password
    """
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        if phone_number is None or password is None:
            return None
        
        # Clean phone number - remove any spaces or dashes
        phone_number = ''.join(filter(str.isdigit, phone_number))
        
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
    
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None 