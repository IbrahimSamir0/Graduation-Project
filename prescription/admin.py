from django.contrib import admin
from .models import *
admin.site.register(Clinical)
admin.site.register(Prescription)
admin.site.register(StandardDrugs)
admin.site.register(Drug)
admin.site.register(Screen)
admin.site.register(StandardScreens)
admin.site.register(TestScreen)
admin.site.register(StandardMedicalAnalysis)
admin.site.register(MedicalAnalysis)
admin.site.register(Booking)
admin.site.register(PatientBooking)
# Register your models here
