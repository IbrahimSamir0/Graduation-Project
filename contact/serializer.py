from rest_framework import serializers
from .models import contactModel

class contactSerializer(serializers.ModelSerializer):
    class Meta:
        model = contactModel
        fields = ['email','text']
        

