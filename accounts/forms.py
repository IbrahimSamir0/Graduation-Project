from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import Patient,Doctor

class PatientSignUpForm(UserCreationForm):
    class Meta:
        model = Patient
        fields = ['first_name','last_name','username','password1','password2']
        
class DoctorSignUpForm(UserCreationForm):
    class Meta:
        model = Doctor
        fields = ['first_name','last_name','username','password1','password2']
        
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields= ['first_name','last_name']
        
        
class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields= ['first_name','last_name','date_birth','phone','city','avatar','doctor_id']


class DoctoProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields= ['first_name','last_name','date_birth','phone','city','avatar']