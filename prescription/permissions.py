from accounts.models import UserType
from rest_framework import permissions


class IsDoctor(permissions.BasePermission):

    def has_permission(self, request, view):
        doctor_type = UserType.objects.get(typ = 2)
        try:
            return bool(request.user and request.user.typ == doctor_type)
        except :
            pass
        

class IsPatient(permissions.BasePermission):

    def has_permission(self, request, view):
        patient_type = UserType.objects.get(typ = 1)
        try:
            return bool(request.user and request.user.typ == patient_type)
        except :
            pass