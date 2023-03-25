from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from .models import Admin, User


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            )
        except User.DoesNotExist:
            pass
        except User.MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password (password) and self.user_can_authenticate(user):
                return user
    
    def getUser(self,user_id):
        try:
            user= User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        return user if self.user.can_authenticate(user) else None
    

class CustomModelBackend(ModelBackend):
    def get_user_model(self):
        if 'createsuperuser' in getattr(settings, 'SHELL_PLUS_COMMANDS', []):
            return Admin
        else:
            return User