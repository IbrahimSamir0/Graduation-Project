from django.shortcuts import redirect,render
from .forms import *
from django.contrib.auth import  authenticate,login, get_user_model
from .models import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm    
from rest_framework.authtoken.models import Token
# Create your views here.
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .helper import activateEmail

    
# @csrf_exempt
def patientSignUp(request):
    if request.method == "POST":
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.typ_id =1
            f.is_active = False
            f.save()
            activateEmail(request, f ,form.cleaned_data.get('username'))
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password1']
            # user =authenticate(username=username , password = password)
            # Token.objects.create(user= user) 
            # login(request , user)
            return redirect('login')
    else :
        form = PatientSignUpForm()
    context = {'form':form}
    return render(request,'registration/sign_up.html',context)



def doctorSignUp(request):
    if request.method == "POST":
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            wait =form.save(commit=False)
            wait.typ_id = 2
            wait.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user =authenticate(username=username , password = password)
            Token.objects.create(user= user) 
            login(request , user)
            return redirect('/accounts/profile/')
    else :
        form = DoctorSignUpForm()
    context = {'form':form}
    return render(request,'registration/login.html',context)




def kindOfProfile(k):
    if k.typ_id == 1 :
        profile = Patient.objects.get(username=k.user)
    elif k.typ_id == 2 :
        profile = Doctor.objects.get(username=k.user)
        
    return(profile)

@login_required()
def profile(request):
    # profile= kindOfProfile(request)
    u = User.objects.get(username=request.user)
    if u.typ_id == 1 :
        profile = Patient.objects.get(username=request.user)
        context = {'profile':profile}
        return render (request ,'accounts/patient_profile.html', context)
    elif u.typ_id == 2 :
        profile = Doctor.objects.get(username=request.user)
        context = {'profile':profile}
        return render (request ,'accounts/doctor_profile.html', context)
    # profile = Patient.objects.get(username=request.user)
    # return render(request, 'accounts/patient_profile.html',{'profile':profile})

# @csrf_exempt
@login_required
def editProfile(request):
    u = User.objects.get(username=request.user)
    
    if u.typ_id == 1 :
        profile = Patient.objects.get(username=request.user)
        if request.method == "POST":
            profile_form = PatientProfileForm(request.POST,request.FILES,instance= profile)   
        else :
        # user_form = UserForm(instance=request.user)
            profile_form = PatientProfileForm(instance=profile)   
        # pass_form = PasswordChangeForm(request.user)
        # pass_form = PasswordChangeForm(request.user,request.POST)
        
    elif u.typ_id == 2 :
        profile = Doctor.objects.get(username=request.user)
        if request.method == "POST":
            profile_form = DoctoProfileForm(request.POST,request.FILES,instance= profile)   
        else :
        # user_form = UserForm(instance=request.user)
            profile_form = DoctoProfileForm(instance=profile)   
        # pass_form = PasswordChangeForm(request.user)
        # pass_form = PasswordChangeForm(request.user,request.POST)
        
    if profile_form.is_valid() :
        profile_form.save()
        # new= pass_form.save()
        # update_session_auth_hash(request,new) # important to hash password and sql injection validation
        # messages.success(request, 'Your data was successfully updated!')
        # return redirect(reverse('accounts:profile'))
        return redirect('/accounts/profile/')
        
    
    
    context = {'profile_form':profile_form}
    return render (request, 'accounts/edit_profile.html',context)

# @csrf_exempt
@login_required
def changePass(request):
    if request.method == "POST":
        pass_form = PasswordChangeForm(request.user,request.POST)
        if pass_form.is_valid():
            new= pass_form.save()
            update_session_auth_hash(request,new) # important to hash password and sql injection validation
            messages.success(request, 'Your data was successfully updated!')
            # return redirect(reverse('accounts:profile'))
            return redirect('/accounts/profile/')

    else:
        pass_form = PasswordChangeForm(request.user)
        
    context = {'pass_form':pass_form}
    return render (request, 'accounts/change_password.html',context)


# def LoginView(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request,user)
#             return redirect('accounts:login')
#     else:
#         form = AuthenticationForm()
#     return render(request,'accounts/login.html', {'form':form})


