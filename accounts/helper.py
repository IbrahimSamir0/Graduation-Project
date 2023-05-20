from django.core.mail import send_mail
import uuid
from django.conf import settings
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import  authenticate,login, get_user_model
from django.contrib import messages
from django.shortcuts import redirect,render
from rest_framework.authtoken.models import Token


def sendForgerPasswordMail(email, token, encoded_pk):
    subject= 'Your forget password link'
    message =f'Hi, click on the link to reset your password http://localhost:8081/newpasswordpg/{encoded_pk}/{token}/'
    from_email = settings.EMAIL_HOST_USER
    recipient_list=[email]
    try:
        send_mail(subject=subject,message= message, from_email=from_email, recipient_list=recipient_list,fail_silently=True)
        # email = EmailMessage(subject, message, to=[email])
        # if email.send():
        return True
    except :
        return False
# accounts:password_reset



def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        Token.objects.create(user= user) 

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('login')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string("registration/template_activate_account.html",{
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request,f'Dear <b>{user}</b>, please go to your email<b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> check your span folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
    