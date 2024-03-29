import uuid
from accounts.helper import activateEmail
from .models import *
from prescription.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework import generics , status, filters ,viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
# from knox.views import LoginView as KnoxLoginView
# from knox.models import AuthToken
from rest_framework.permissions import IsAuthenticated   ,AllowAny
from twilio.rest import Client
from django.http import JsonResponse
import random
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse 
from django.shortcuts import redirect,render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status, viewsets, response
from . import serializers
from django.core import serializers as Serializers
from .helper import sendForgerPasswordMail
from rest_framework.decorators import action
import json
from prescription.permissions import *
from rest_framework.pagination import PageNumberPagination

# patient_type = UserType.objects.get(typ = 1)
# doctor_type = UserType.objects.get(typ = 2)


# from knox.models import AuthToken

# class LoginApi(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         context = dict(request=request, view=self)
#         serializer = self.serializer_class(data=request.data, context=context)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         # update_last_login(None, user, )
#         token = MultiToken.objects.create(user=user)
#         data = {'token': token.key}

#         return Response(data)

########################################################## PATIENT ####################################################
@api_view(['GET','POST'])
# @authentication_classes([TokenAuthentication])
def patient_list(request):
    # GET
    if request.method == 'GET':    
        all_patient= Patient.objects.all()
        all_patient_data = PatientSerializer(all_patient, many=True)
        return Response(all_patient_data.data)
    #POST
    elif request.method == 'POST':
        all_patient= Patient.objects.all()
        all_patient_data = PatientSerializer(all_patient, many=True)
        patient_data =PatientSerializer(data= request.data)
        if (patient_data.is_valid()):
            new =patient_data.password
            update_session_auth_hash(request,new)
            patient_data.save()
            return Response(all_patient_data.data,status= status.HTTP_201_CREATED)
        return Response(patient_data.data,status= status.HTTP_400_BAD_REQUEST)
    
    
# class PatientList(generics.ListCreateAPIView):
#     queryset=Patient.objects.all()
#     serializer_class=PatientSerializer
#     authentication_classes=[TokenAuthentication]


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def FBV_pk_patient(request,id):
    try:
        patient = Patient.objects.get(id = id)
    except Patient.DoesNotExist:
        return Response({"status":False,"data":None,"message":"No patient with this id"},status= status.HTTP_404_NOT_FOUND)
    #GET
    if request.method == 'GET':    
        patient_data = PatientSerializer(patient)
        return Response({"status":True,"data":patient_data.data,"message":"No patient with this id"},status=
                        status.HTTP_200_OK)
    
    # #PUT
    # elif request.method == 'PUT':
    #     patient_data =PatientSerializer(patient,data= request.data)
    #     if (patient_data.is_valid()):
    #         patient_data.save()
    #         return Response(patient_data.data)
    #     return Response(Patient.errors,status= status.HTTP_400_BAD_REQUEST)
    
    # #DELETE
    # elif request.method == 'DELETE':    
    #     patient.delete()
    #     return Response(status= status.HTTP_204_NO_CONTENT )


########################################################## DOCTOR ####################################################

class CustomPagination(PageNumberPagination):
    page_size = 3


class GetAllDoctors(generics.ListAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsPatient,]
    serializer_class = DoctorSerializer
    pagination_class = CustomPagination
    def get(self, request):
        # GET
        try:
            #Select All Doctors that have booking
            queryset = Doctor.objects.filter(booking__isnull=False).distinct()
        except Doctor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Apply pagination to queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return Response({"status":True,
                             "count": queryset.count(),
                            "next": self.paginator.get_next_link(),
                            "previous": self.paginator.get_previous_link(),
                             "data":serializer.data,
                             "message":"Success"}
                            ,status=status.HTTP_200_OK)

        serializer = self.serializer_class(queryset, many=True)
        return Response({"status":True,
                             "count": queryset.count(),
                            "next": None,
                            "previous": None,
                             "data":serializer.data,
                             "message":"Success"}
                            ,status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsPatient])
def searchDoctor(request):
    # GET
    if request.method == 'POST':
        data=request.data
        try:
            doctor= Doctor.objects.filter(**data,booking__isnull=False).distinct()
        except Doctor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DoctorSerializer(doctor, many=True)
        return Response({"status":True,"data":serializer.data,"message":"Success"},status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def FBV_pk_doctor(request,id):
    try:
        doctor = Doctor.objects.get(id = id)
    except Doctor.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
    #GET
    if request.method == 'GET':    
        serializer = DoctorSerializer(doctor)
        if Prescription.objects.filter(patient=request.user.id, doctor=doctor).exists():
            return Response({"status":True,
                             "data":serializer.data,
                             "p_id":request.user.id,
                             "isCanRate":True,
                             "message":"Success"},status=status.HTTP_200_OK)    
        else:
            return Response({"status":True,
                             "data":serializer.data,
                             "p_id":request.user.id,
                             "isCanRate":False,
                             "message":"Success"},status=status.HTTP_200_OK)
    # #PUT
    # elif request.method == 'PUT':
    #     doctor_data =DoctorSerializer(doctor,data= request.data)
    #     if (doctor_data.is_valid()):
    #         doctor_data.save()
    #         return Response(doctor_data.data)
    #     return Response(Doctor.errors,status= status.HTTP_400_BAD_REQUEST)
    
    # #DELETE
    # elif request.method == 'DELETE':    
    #     doctor.delete()
    #     return Response(status= status.HTTP_204_NO_CONTENT )
    
    
class SendOTP(APIView):
    def post(self , request):
        account_sid =""
        auth_token = ""
        phone=request.data['phone']
        client = Client(account_sid,auth_token)
        otp=generateOTP()
        body ="Your OTP is: "+str(otp)
        message= Client.messages.create(from_="", body = body, to=phone)
        if message.sid:
            print('send successful')
            return JsonResponse({"success":True})
        else:
            print('send fail')
            return JsonResponse({"success":False})
            
def generateOTP():
    return random.randrange(100000,999999)


class RegisterAsPatientAPI(generics.CreateAPIView):
    # queryset = Patient.objects.all()
    serializer_class = RegisterSerializerAsPatient
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        activateEmail(request, user ,serializer.validated_data.get('email'))
        return Response({
        # "user": DoctorSerializer(user, context=self.get_serializer_context()).data,
        # "token": Token.objects.get(user =user).key
        }, status= status.HTTP_201_CREATED)
        
class MyProfilePatient(generics.ListAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    serializer_class = PatientSerializer
    def get(self, request):
        try:
            patient = Patient.objects.get(id = request.user.id)
        except Exception as e :
            return Response(f'{e}',status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(patient,many=False)
        return Response({"status":True,
                         "data":serializer.data,
                         "message":"Success"},
                        status=status.HTTP_200_OK)
            
        
class EditPatientProfile (generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    serializer_class= EditPatientProfileSerializer
    def put (self, request, *args, **kwargs):
        try:
            patient = Patient.objects.get(id= request.user.id)
        except Exception as e:
            return Response(f'{e}',status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(patient)
        serializer = self.serializer_class(patient,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response ({"status":True,"data":serializer.data,"message":"Success"},status=status.HTTP_200_OK)
    
        
class RegisterAsDoctorAPI(generics.CreateAPIView):
    # queryset = Doctor.objects.all()
    serializer_class = RegisterSerializerAsDoctor
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        activateEmail(request, user ,serializer.validated_data.get('email'))
        return Response({
        # "user": DoctorSerializer(user, context=self.get_serializer_context()).data,
        "token": Token.objects.get(user =user).key
        }, status= status.HTTP_201_CREATED)

class EditDoctorProfile(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    serializer_class = EditDoctorProfileSerializer
    def get(self, request):
        doctor = Doctor.objects.get(id= request.user.id)
        serializer = self.serializer_class(doctor)
        return Response({"status":True,"data":serializer.data,"message":"Success"},status=status.HTTP_200_OK)
    
    def put (self, request, *args, **kwargs):
        doctor = Doctor.objects.get(id= request.user.id)
        serializer = self.serializer_class(doctor,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response ({"status":True,"data":serializer.data,"message":"Success"},status=status.HTTP_200_OK)


class MyProfileDoctor(generics.ListAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    serializer_class = DoctorSerializer
    def get(self, request):
        try:
            doctor = Doctor.objects.get(id = request.user.id)
        except Exception as e :
            return Response(f'{e}',status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(doctor,many=False)
        return Response({"status":True,"data":serializer.data,"message":"This is your profile"}, status=status.HTTP_200_OK)
            
class DoctorRate(generics.CreateAPIView, generics.DestroyAPIView):
    # queryset= Doctor.objects.all()
    permission_classes = [IsPatient,]
    serializer_class = RatingSerializer
    authentication_classes = [TokenAuthentication,]

    def post(self, request, id ):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            doctor= Doctor.objects.get(id=id)
        except Doctor.DoesNotExist:
            return response(status=status.HTTP_404_NOT_FOUND)
        # doctor = request.data['doctor']
        patient = Patient.objects.get(id= request.user.id)
        stars =serializer.validated_data['stars']
        feedback = serializer.validated_data['feedback']        
        try:# Update if old rating
            rating = Rating.objects.get(patient = patient, doctor= doctor)
            rating.stars = stars
            rating.feedback = feedback
            rating.save()
            
            # data =serializer(rating, many=False).data
            json ={
                'message':'Doctor rate updated.',
                # 'result': rating
            }
            return Response(json,status=status.HTTP_200_OK)

        except: #create
            rating = Rating.objects.create(stars=stars, doctor=doctor, patient=patient, feedback=feedback)
            # data = RatingSerializer(rating, many=False)   
            json ={
                'message':'Doctor rate created.',
                # 'result': data
            }
            return Response(json,status=status.HTTP_201_CREATED)
            
        else :
            json ={
                'message':'Doctor rate not send',
            }
            return Response(json,status=status.HTTP_400_BAD_REQUEST)
    def delete ( self,request, id):
        try:
            doctor= Doctor.objects.get(id=id)
        except Doctor.DoesNotExist:
            return response(status=status.HTTP_404_NOT_FOUND)
        # doctor = request.data['doctor']
        patient = Patient.objects.get(id= request.user.id)
        rate = Rating.objects.get(patient=patient, doctor=doctor)
        rate.delete()
        return Response(status=status.HTTP_200_OK)
                        
class RatingAPI(viewsets.ModelViewSet):
    queryset= Rating.objects.all()
    serializer_class = RatingSerializer
  
    
# class LoginAPI(generics.CreateAPIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = AuthTokenSerializer
#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         try:
#             user_obj = User.objects.get(username=user)
#         except Exception :
#             user_obj = User.objects.get(email = user)

#         try:
#             token = Token.objects.get(user=user)
#         except Token.DoesNotExist:
#             return Response({'message':"Token not found"},status=status.HTTP_404_NOT_FOUND)   
#         login(request, user)
#         return Response({"accesToken": token.key,'type':user_obj.typ.typ},status=status.HTTP_200_OK)


class LoginAPI(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try :
            token, created = Token.objects.get_or_create(user=user)
        except:
            return Response({"status":False,
                             "data":None,
                             "message":"Username Or Password is Wrong."},
                            status=status.HTTP_404_NOT_FOUND)
        # login(request,user)
        return Response({"status":True,
                         "data":{
                            'accesToken': token.key,
                            'user_id': user.pk,
                            'type': user.typ.typ
                            },
                         "message":"login success."
        },status=status.HTTP_200_OK)

class LogoutAPI(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    def delete(self,request):
        user = User.objects.get(id=request.user.id)
        token = Token.objects.get(user=user)
        token.delete()
        return Response("Successful logout", status=status.HTTP_200_OK)

class ChangePasswordView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordSerializer
    model = User
    # authentication_classes =(TokenAuthentication,)
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
            
        if serializer.is_valid() :
            if serializer.validated_data['new_password'] == serializer.validated_data['confirm_new_password']:
            # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
                return Response(response)
            return Response({"confirm_new_password": ["Doesn't match new password."]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordReset(generics.GenericAPIView):
    """
    Request for Password Reset Link.
    """

    serializer_class = serializers.EmailSerializer

    def post(self, request):
        """
        Create token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        try:
            user = User.objects.get(email=email)
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            # redirect("api/password_reset/",)
            # reset_url = reverse("accounts:password_reset",kwargs={"encoded_pk": encoded_pk, "token": token},)
            # reset_link = f"http://127.0.0.1:8000{reset_url}"
            temp=sendForgerPasswordMail(email,token,encoded_pk)
            # send the rest_link as mail to the user.

            return response.Response(
                {
                    "message": 
                    f"You will found password reset link in your email.<br>Hint: Check spam messages"
                },
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return response.Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordAPI(generics.GenericAPIView):
    """
    Verify and Reset Password Token View.
    """

    serializer_class = serializers.ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        """
        Verify token & encoded_pk and then reset the password.
        """
        serializer = self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )
        serializer.is_valid(raise_exception=True)
        return response.Response(
            {"message": "Password reset complete"},
            status=status.HTTP_200_OK,
        )
        
# # api_view['POST']
# # def forgetPassword(request):
# #     if request.method =='POST':
# #         email =request.POST.get['email']
# #         if not User.objects.get(email=email):
            
            
               
# class ForgetPassword(generics.CreateAPIView):
#     serializer_class = EmailSerializer
#     model = User
    
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.data["email"]
#         user = User.objects.get(email=email)
#         if user:
#             # encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
#             forgetPass(request, user ,serializer.validated_data.get('email'))

#             return response.Response({"message": "Email sent succesfully!"},status=status.HTTP_200_OK,)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class ChangePasswordAfterForget (generics.UpdateAPIView):
#     serializer_class= ChangePasswordAfterForgetSerializer
#     model =User
#     def update(self,request,token):
#         try:
#             user =User.objects.filter(token=token).first()
        
#             serializer = self.serializer_class(data=request.data)
#             if serializer.is_valid()  :
#                 if serializer.validated_data['new_password'] == serializer.validated_data['confirm_new_password']:
#                     # set_password also hashes the password that the user will get
#                     user.set_password(serializer.data.get("new_password"))
#                     user.save()
#                     response = {
#                         'status': 'success',
#                         'code': status.HTTP_200_OK,
#                         'message': 'Password updated successfully',
#                         'data': []
#                     }
#                     return Response(response)
#                 return Response({"confirm_new_password": ["Doesn't match new password."]}, status=status.HTTP_400_BAD_REQUEST)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except User.DoesNotExist :
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ClinicalVeiw(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication,]
    permission_classes=[AllowAny,]
    serializer_class = CitySerializer
    def get(self,request):
        cities = City.objects.all()
        serializer = self.serializer_class(cities, many=True)
        return Response ({"status":True,
                          "data":serializer.data,
                          "message":"Success"},
                         status=status.HTTP_200_OK)