from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from .validate import Validation
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from datetime import date
from django.utils import timezone

# from prescription.models import Booking
# Create your models here.

validate = Validation()
def future_date_validator(value):
    if date.today() < value:
        raise ValidationError("Date cannot be in the future.")

def phoneValidate(value):
    numbers ='0123456789'
    if len(value) == 11:
        if value[0]=='0' and value[1]=='1' and (value[2]=='0' or value[2]=='1' or value[2]=='2' or value[2]=='5'):
            for i in value:
                if i not in numbers:
                    raise ValidationError(
                        _('%(value)s is not a phone number'),
                        params={'value': value},
                    )
        else:
            raise ValidationError(
                        _('%(value)s is not a phone number'),
                        params={'value': value},
                    )
    else:
            raise ValidationError(
                        _('%(value)s is length is less than 11 numbers.'),
                        params={'value': value},
                    )
        
def doctorValidate(value):
    pass
        

def image_upload(instance, filename):
    imagename , extension = filename.split(".")
    return "avatar/%s.%s"%(instance.id,extension)



CITIES=(
    ('Cairo','Cairo'),
    ('Alexandria','Alexandria'),
    ('Giza','Giza'),
    ('Shubra El Kheima','Shubra El Kheima'),
    ('Port Said','Port Said'),
    ('Suez','Suez'),
    ('El Mahalla El Kubra','El Mahalla El Kubra'),
    ('Luxor','Luxor'),
    ('Mansoura','Mansoura'),
    ('Tanta','Tanta'),
    ('Asyut','Asyut'),
    ('Ismailia','Ismailia'),
    ('Faiyum','Faiyum'),
    ('Zagazig','Zagazig'),
    ('Damietta','Damietta'),
    ('Aswan','Aswan'),
    ('Minya','Minya'),
    ('Damanhur','Damanhur'),
    ('Beni Suef','Beni Suef'),
    ('Hurghada','Hurghada'),
    ('Qena','Qena'),
    ('Sohag','Sohag'),
    ('Shibin El Kom','Shibin El Kom'),
    ('Banha','Banha'),
    ('Arish','Arish'),
    ('Qalyubia','Qalyubia'),
    ('Gharbia','Gharbia'),
)

    
class CustomUserManger(BaseUserManager):   
    
    def create_user(self, email, password, **extra_fields): 
        # if typ == 1:   
        #     extra_fields.setdefault('typ_id',1)
        # elif typ ==2:
        #     extra_fields.setdefault('typ_id',2)
            
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        # Token.objects.create(user)
        Token.objects.create(user = user)   
        return user
    

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('typ_id',0)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser has to have is_staff is True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser has to have is_superuser is True")
        if extra_fields.get('typ_id') != 0:
                raise ValueError("Superuser has to have type is 0")
        return self.create_user(email=email, password=password, **extra_fields)
    

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(unique=True, max_length=30,null=True)
    email = models.EmailField(unique=True)
    is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    typ = models.ForeignKey("UserType",on_delete=models.PROTECT) 
    # typ = models.IntegerField(primary_key=True,default=0)  
    
    objects= CustomUserManger()
    
    USERNAME_FIELD='username'
    EMAIL_FIELD ='email'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        # abstract = True
        
    
    def __str__(self) :
        return self.username
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.email.split('@')[0]


class UserType(models.Model):
    typ = models.PositiveSmallIntegerField(primary_key=True)  
    type_name = models.CharField(_("type name"), max_length=20)

    def __str__(self) :
        return self.type_name
    
    
class UserInheritance(models.Model):
    GENDER= (
        ('M','M'),
        ('F','F'),
        )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_birth = models.DateField(validators= [future_date_validator])
    phone = models.CharField(max_length=11,validators=([phoneValidate]))
    city = models.CharField(max_length=30, choices=CITIES)
    avatar = models.TextField(blank= True)
    gender = models.CharField(choices=GENDER, max_length=1)
    
        
    def get_age (self):
        today = date.today()
        if self.date_birth is not None :
            return int((today- self.date_birth).days/365)
        else : return 0 
        
    class Meta:
        abstract = True

class Admin(User,UserInheritance):
    # is_superuser =models.BooleanField(default=True)

    # objects= CustomUserManger()
    
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
    #     db_table ='admin'

    
class Patient (User,UserInheritance):
    doctor_id = models.ForeignKey("Doctor", verbose_name=("Doctor_id"), on_delete=models.CASCADE,blank=True, null=True)
    # booking = models.ForeignKey('prescription.Booking',on_delete=models.PROTECT,blank=True, null=True)
    # def get_age ():
    #     age= UserInheritance.objects.get()
        
    def __str__(self) :
        return self.username       
    
    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        # db_table ='patient'

class Doctor(User,UserInheritance):
    # doctor_number = models.CharField(max_length=10,unique=True,validators=[doctorValidate])
    price = models.PositiveIntegerField(default=0)
    bio = models.CharField(max_length=100,null=True,blank=True)
    about = models.TextField(null=True,blank=True)
    # clinical = models.ManyToManyField("prescription.Clinical", verbose_name=_("Clinical"))
    def __str__(self) :
        return self.username
    
    def numOfRating(self):
        rating = Rating.objects.filter(doctor=self)
        return len(rating)
    
    def ratingDetails(self):
        rating = Rating.objects.filter(doctor =self,feedback__isnull=False).order_by('-id')[:12]
        ratingDetails=[]
        for r in rating:
            all_name=r.patient.first_name+' '+r.patient.last_name
            p_id=r.patient.id
            s={"p_id":p_id,"name":all_name,"stars":r.stars,"feedback":r.feedback,'date':r.date}
            ratingDetails.append(s)
        return ratingDetails
    
    def avgRating(self):
        sum = 0    
        rating = Rating.objects.filter(doctor=self)

        for x in rating:
            sum+= x.stars
        
        if len(rating) > 0:
            return sum/ len(rating)
        else:
            return 0

    
    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        # db_table ='doctor'
        
        
class Rating (models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    feedback = models.TextField(null=True,blank=True)
    date =models.DateField(default=timezone.now)
    
    class Meta:
        unique_together =(('doctor','patient'),)
        index_together =(('doctor','patient'),)
        
    def __str__(self):
        return self.doctor.username
    
    

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "ebrahim.ssamer77@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
