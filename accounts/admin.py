from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
# Register your models here.

# admin.site.register(User)
admin.site.register(Admin)
admin.site.register(PatientDiseases)
admin.site.register(PatientDrug)
admin.site.register(City)
# admin.site.register(Doctor)

# admin.site.unregister(Group)


class RatingAdmin(admin.ModelAdmin):
    list_display = ['id','doctor','patient','stars']
    search_fields = ['username','first_name','last_name']
    list_filter=['doctor','patient']
    
class DoctorAdmin (admin.ModelAdmin):
    list_display = ['id','username','first_name','last_name','phone']
    search_fields = ['username','first_name','last_name']
    list_filter = ['username','first_name']


class PatientAdmin (admin.ModelAdmin):
    list_display = ['id','username','first_name','last_name','phone']
    search_fields = ['username','first_name','last_name']
    list_filter = ['username','first_name','last_name']

admin.site.register(Rating, RatingAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)