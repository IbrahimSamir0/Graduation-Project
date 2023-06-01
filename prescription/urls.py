from django.urls import include,path
from . import views


app_name='prescription'


urlpatterns = [
    # path('make_prescription/',views.makePrescription, name='create_prescription'),
    # path('create_prescription',views.MakePrescription.as_view({'get': 'list','post':'create'}), name='create_prescription'),
    # path('postScreen/',views.PostScreen.as_view(), name='postScreen'),
    # path('view',views.viewOldPrescriptions, name='ViewOldPrescriptions'),
    # path('postscreens/',views.upload_image, name='PostScreen'),
    
    path('get_active_doctor_patients/',views.GetActiveDoctorPatients.as_view(), name='GetActiveDoctorPatients'),
    # path('get_old_doctor_patients/',views.GetOldDoctorPatients.as_view(), name='GetOldDoctorPatients'),
    path('get_all_doctor_patients/',views.GetAllDoctorPatients.as_view(), name='GetAllDoctorPatients'),
    
    path('get_all_booked_patients/',views.GetAllBookedPatients.as_view(), name='GetBookedPatients'),
    path('get_specific_clinic_booked_patients/<int:id>/',views.GetBookedPatientsInSpecificClinic.as_view(), name='GetBookedPatientsInEachClinic'),
    path('get_specific_appointment_booked_patients/<int:id>/',views.GetBookedPatientsInSpecificBooking.as_view(), name='GetBookedPatientsInEachClinic'),
    path('get_Today_booked_patients/',views.GetTodayBookedPatientsInClinic.as_view(), name='GetBookedPatientsInEachClinic'),
    path('get_Today_booked_patients_first_10/',views.GetTodayBookedPatientsInClinicFirst10.as_view(), name='GetTodayBookedPatientsInClinicFirst10'),
    
    path('drug_deteails/',views.DrugDeteails.as_view(),name='DrugDeteails'),
    path('get_interAction/',views.GetInterAction.as_view(),name='DrugDeteails'),
    path('get_my_all_clinics/',views.ListClinical.as_view(),name='ListClinical'),
    path('get_my_all_clinics/<int:id>/',views.GetSpecificClinical.as_view(),name='ListClinical'),
    path('get_doctor_patient_specific_prescription/<int:p_id>/',views.GetSpecificDoctorPatientPrescription.as_view(), name='GetSpecificDoctorPatientPrescription'),
    path('cancel_my_Prescription/',views.CancelMyPrescription.as_view(), name='cancel_my_Prescription'),
    path('get_my_active_prescription/',views.GetMyActivePrescription.as_view(), name='GetMyActivePrescription'),
    path('get_my_old_prescriptions/',views.GetMyOldPrescriptions.as_view(), name='GetMyOldPrescriptions'),
    path('get_my_old_prescriptions/<int:p_id>/',views.GetSpecificOldPrescription.as_view(), name='GetSpecificOldPrescription'),
    path('set_appointment_for_doctors/',views.SetAppointmentForDoctors.as_view(), name='SetAppointmentForDoctors'),
    path('modify_appointment_for_doctors/<int:id>/',views.ModifySpecificAppointmentForDoctor.as_view(), name='ModifySpecificAppointmentForDoctor'),
    path('get_appointments_for_doctors/',views.GetMyAllAppointmentsForDoctor.as_view(), name='GetMyAllAppointmentsForDoctor'),
    path('get_appointments_for_doctor/<int:id>/',views.GetAllAppointmentsForDoctor.as_view(), name='GetAllAppointmentsForDoctor'),
    
    path('get_appointments_for_patient/<int:d_id>/<int:id>/',views.GetMyAllAppointmentsForPatient.as_view(), name='GetMyAllAppointmentsForPatient'),
    path('book/<int:id>/',views.BookingApi.as_view(),name='BookingApi'),
    
    path('get_all_standard_drugs/',views.GetAllStandardDrugsName.as_view(),name='GetAllStandardDrugsName'),
    path('get_all_standard_drugs_name_filter/',views.GetAllStandardDrugsNameFilter.as_view(),name='GetAllStandardDrugsName'),
    path('get_my_screens/',views.GetMyScreens.as_view(),name='GetMyOldPrescriptions'),
    path('update_my_screen/<int:id>/',views.AddOrUpdateScreenForPatient.as_view(),name='AddOrUpdateScreenForPatient'),
    path('get_my_serial_films/<int:id>/',views.GetSerialFilmView.as_view(),name='GetSerialFilmView'),
    
    # path('get_my_screens/<int:id>/',views.GetMySpecificScreens.as_view(),name='GetMySpecificOldScreens'),
    # path('get_my_active_screeen/',views.GetMyActiveScreen.as_view(),name='GetMyActivePrescription'),
    path('get_my_tests/',views.GetMyMedicalAnlaysis.as_view(),name='GetMyMedicalAnlaysis'),
    path('update_my_test/<int:id>/',views.AddOrUpdateMedicalAnalysisForPatient.as_view(),name='AddOrUpdateMedicalAnalysisForPatient'),
    # path('get_my_test/<int:id>/',views.GetMySpecificScreens.as_view(),name='GetMySpecificOldScreens'),    
    
    path('get_my_diseases/',views.MyPatientDisease.as_view()),
    path('get_my_diseases/<int:id>/',views.SpecificPatientDiseaseView.as_view()),
    path('get_patient_diseases_for_doctor/<int:id>/',views.GetPatientDiseaseView.as_view()),
    path('get_patient_drugs_for_doctor/<int:id>/',views.GetPatientDrugsView.as_view()),
    path('get_all_chronic_diseases/',views.ChronicDiseaseView.as_view()),
    path('get_all_standard_screens/',views.StandardScreensView.as_view()),
    path('get_all_standard_tests/',views.StandardTestView.as_view()),
    
    path('commitment/<int:id>/',views.CommitmentView.as_view()),
    
    path('PatientDrugView/',views.PatientDrugView.as_view()),
    path('PatientDrugView/<int:id>/',views.PatientDrugDeleteView.as_view()),
    
    path('ImageEditorView/<int:id>/',views.ImageEditorView.as_view()),
    
    
    # path('set_drug/',views.SetDrug.as_view(), name='SetDrug'),   
]