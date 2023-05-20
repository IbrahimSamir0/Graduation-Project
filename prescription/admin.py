from django.contrib import admin
from .models import *
admin.site.register(Clinical)
admin.site.register(Prescription)
admin.site.register(StandardDrugs)
admin.site.register(Drug)
admin.site.register(Screen)
admin.site.register(StandardScreens)
admin.site.register(StandardMedicalAnalysis)
admin.site.register(MedicalAnalysis)
admin.site.register(Booking)
admin.site.register(ChronicDiseases)
admin.site.register(PatientBooking)
admin.site.register(PatientCommitment)
admin.site.register(active_Ingredient)
# Register your models here
