from rest_framework import  serializers
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
# from django.contrib.auth import authenticate, get_user_model
# from django.utils.translation import gettext_lazy as _


class Type(serializers.ModelSerializer):
    class Meta:
        model= UserType
        fields=['type_name']
        

class DoctorSerializer(serializers.ModelSerializer):
    # user_type = Type()
    class Meta:
        model = Doctor
        fields = ['username','first_name','last_name','phone','avatar','bio','about','city','price','numOfRating','avgRating','ratingDetails']
        
class EditDoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields=['username','first_name','last_name','city','price','avatar','bio','about']
    
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id','doctor_id','email','username','first_name','last_name','get_age','phone','avatar','city']
        # extra_kwargs = {'password': {'write_only': True}}
        
class EditPatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['username','first_name','last_name','avatar','city']

class ConfirmPasswordSerializer(serializers.Serializer):
    password_confirm = serializers.CharField(required = True)


# class LoginSerializers(serializers.Serializer):
#     email = serializers.CharField(max_length=255)
#     password = serializers.CharField(
#         label=_("Password"),
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#         max_length=128,
#         write_only=True
#     )

#     def validate(self, data):
#         username = data.get('email')
#         password = data.get('password')

#         if username and password:
#             user = authenticate(request=self.context.get('request'),
#                                 username=username, password=password)
#             if not user:
#                 msg = _('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = _('Must include "username" and "password".')
#             raise serializers.ValidationError(msg, code='authorization')

#         data['user'] = user
#         return data
    
    
class RegisterSerializerAsPatient(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id','email','password','first_name','last_name','phone','date_birth')
        extra_kwargs = {'password': {'write_only': True}}

    # def createPatient(self, validated_data):  
    #     user = Patient.objects.create_user(validated_data['username'],  validated_data['password'],validated_data['typ'])
    #     return user
    
    def create(self, validated_data):
        patient_type = UserType.objects.get(typ = 1)
        # def split(email):
        #     username, domain = email.split("@"),
        #     return username
        user = Patient(
            email=validated_data['email'] ,
            username =validated_data['email'].split('@')[0],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            typ=patient_type,
            phone=validated_data['phone'],
            
            # is_active =False,
            password = make_password(validated_data['password'])
        )
        user.save()
        Token.objects.get_or_create(user=user)
        return user
    
class RegisterSerializerAsDoctor(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id','email','password','first_name','last_name','phone')
        extra_kwargs = {'password': {'write_only': True}}

    # def createdoctor(self, validated_data):  
    #     user = Doctor.objects.create_user(validated_data['username'],  validated_data['password'],validate_data['typ'])
    #     return user
    def create(self, validated_data):
        doctor_type = UserType.objects.get(typ = 2)
        
        user = Doctor(
            email=validated_data['email'] ,
            username =validated_data['email'].split('@')[0],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            typ=doctor_type,
            phone=validated_data['phone'],
            
            # is_active =False,
            # doctor_number=validated_data['doctor_number'],
            password = make_password(validated_data['password'])
        )
        user.save()
        Token.objects.get_or_create(user=user)
        return user
    
class RatingSerializer(serializers.ModelSerializer):
    class Meta :
        model = Rating
        fields = ['stars','feedback']
        
class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password =serializers.CharField(required =True)
    
class EmailSerializer(serializers.Serializer):
    """
    Reset Password Email Request Serializer.
    """

    email = serializers.EmailField()

    class Meta:
        fields = ("email",)



class ResetPasswordSerializer(serializers.Serializer):
    """
    Reset Password Serializer.
    """

    password = serializers.CharField(
        write_only=True,
        min_length=1,
    )

    class Meta:
        field = ("password")

    def validate(self, data):
        """
        Verify token and encoded_pk and then set new password.
        """
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(password)
        user.save()
        return data
    
class ChangePasswordAfterForgetSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_new_password =serializers.CharField(required =True)