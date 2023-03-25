from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
    
class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return True