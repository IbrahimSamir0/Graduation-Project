from django.urls import path
from contact import views 

app_name='contact'

urlpatterns = [
    path('contact/',views.contactGET),
    path('contactpost/',views.contactPOST),
]
