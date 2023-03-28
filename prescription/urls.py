from django.urls import include,path
from . import views


app_name='prescription'


urlpatterns = [
    # path('make_prescription/',views.makePrescription, name='create_prescription'),
    # path('create_prescription',views.MakePrescription.as_view({'get': 'list','post':'create'}), name='create_prescription'),
    path('postScreen',views.postScreen, name='postScreen'),
    # path('view',views.viewOldPrescriptions, name='ViewOldPrescriptions'),
    path('postscreens',views.upload_image, name='PostScreen'),
    path('get_doctor_patients/',views.GetDoctorPatients.as_view(), name='GetDoctorPatients'),
    path('get_doctor_patients/<int:p_id>/',views.GetSpecificDoctorPatientPrescription.as_view(), name='GetSpecificDoctorPatientPrescription'),
    path('getscreen',views.GetScreen.as_view(), name='GetScreen'),
    path('cancel_my_Prescription/',views.CancelMyPrescription.as_view(), name='cancel_my_Prescription'),
    path('get_my_active_prescription/',views.GetMyActivePrescription.as_view(), name='GetMyActivePrescription'),
    path('get_my_old_prescriptions/',views.GetMyOldPrescriptions.as_view(), name='GetMyOldPrescriptions'),
    path('get_my_old_prescriptions/<int:p_id>/',views.GetSpecificOldPrescription.as_view(), name='GetSpecificOldPrescription'),
    path('set_appointment_for_doctors/',views.SetAppointmentForDoctors.as_view(), name='SetAppointmentForDoctors'),
    path('modify_appointment_for_doctors/<int:id>',views.ModifySpecificAppointmentForDoctor.as_view(), name='ModifySpecificAppointmentForDoctor'),
    path('get_appointments_for_doctors/',views.GetMyAllAppointmentsForDoctor.as_view(), name='GetMyAllAppointmentsForDoctor'),
    path('get_all_standard_drugs/',views.GetAllStandardDrugsName.as_view(),name='GetAllStandardDrugsName'),
    path('get_all_standard_drugs_name_filter/',views.GetAllStandardDrugsNameFilter.as_view(),name='GetAllStandardDrugsName'),
    # path('set_drug/',views.SetDrug.as_view(), name='SetDrug'),   
]