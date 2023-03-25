from django.shortcuts import redirect,render
from .forms import *
from django.contrib.auth import authenticate ,login
from .models import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def doctorSignUp(request):
    if request.method == "POST":
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user =authenticate(email=email , password = password)
            login(request , user)
            return redirect('/accounts/doctor_profile/')
    else :
        form = DoctorSignUpForm()
    context = {'form':form}
    return render(request,'registration/sign_up.html',context)



@login_required
def doctorProfile(request):
    # profile=Patient.objects.get(Patient)
    print(request.user)
    profile = Doctor.objects.get(email=request.user)
    context = {'profile':profile}
    return render (request ,'accounts/profile.html', context)
