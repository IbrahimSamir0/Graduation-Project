from django.urls import include,path
from . import views
from . import helper
from . import api
# from prescription import views
# from knox import views as knox_views
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

app_name='accounts'

# router = routers.DefaultRouter()
# router.register('Rating',api.RatingAPI)
# router.register('doctor_profile',api.DoctorViewSet)
# router.register('Rating',api.RegisterAsPatientAPI)
# router.register('Rating',api.RegisterAsDoctorAPI)



urlpatterns = [
    # path ('',include(router.urls)),
    # path('signup_as_patient',views.patientSignUp, name='signup'),
    path('signup_as_doctor',views.doctorSignUp, name='signup_as_doctor'),
    # path('profile/',views.profile, name='patient_profile'),
    # path('profile/edit/',views.editProfile, name='edit_profile'),
    # path('profile/edit/change_password',views.changePass, name='edit_profile'),
    # path('activate/<uidb64>/<token>', helper.activate, name='activate'),
    path('oauth/', include('social_django.urls', namespace='social')),  # <-- here
       
        # #API
    path('api/patient_profile/register/',api.RegisterAsPatientAPI.as_view()),
    path('api/patient_profile/edit/',api.EditPatientProfile.as_view()),
    path('api/patient_my_profile/',api.MyProfilePatient.as_view(), name='MyProfilePatient'),
    path('api/my_patient_profile/',api.patient_list, name='PatientListAPI'),
    path('api/my_patient_profile/<int:id>',api.FBV_pk_patient, name='PatientprofileDetailAPI'),
    # path('api/my_patient_profile/<int:patient_id>/make_prescription/',views.SetPrescription.as_view(), name='PatientprofileDetailAPI'),
    
    # path('api/get_doctor_clinicals/',views.GetCurentClinicalForPatient.as_view(),name='GetCurentClinicalForPatient'),
    
    path('api/doctor_profile/register/',api.RegisterAsDoctorAPI.as_view()),
    path('api/doctor_profile/edit/',api.EditDoctorProfile.as_view()),
    path('api/doctor_my_profile/',api.MyProfileDoctor.as_view(), name='MyProfileDoctor'),
    path('api/all_doctors_profile/',api.doctorProfileForPatient, name='all_doctors_profile'),
    path('api/doctor_profile/<int:id>/',api.FBV_pk_doctor, name='DoctorDetailAPI'),
    path('api/doctor_profile/<int:id>/rate/',api.DoctorRate.as_view()),
    
    # path('api/patient_profile_class/', api.PatientList.as_view(), name='patientlistClass'),
    
    
    #with token
    path('api_token_auth/patient_profile/',obtain_auth_token,name='auth_token'),
    path('api/login/', api.LoginAPI.as_view(), name='api_login'),
    path('api/logout/', api.LogoutAPI.as_view(), name='api_logout'),
    # path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    
    
    path('api/change_password/', api.ChangePasswordView.as_view(), name='change-password'),
    path("api/password_reset/", api.PasswordReset.as_view(), name="request-password-reset"),
    path("api/password_reset/<str:encoded_pk>/<str:token>/", api.ResetPasswordAPI.as_view(), name="password_reset"),
    # path('api/forget_password/', api.ForgetPassword.as_view(), name='forget-password'),
    # path('api/forget_password/<token>', api.ForgetPassword.as_view(), name='forget-password'),
    

]
