from django.db import models
from accounts.models import Doctor, Patient
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from datetime import date , timedelta
from threading import Timer
from django.db import connection
import base64
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Count


# Create your models here.


def future_date_validator(value):
    if date.today() >= value:
        raise ValidationError("Date cannot be today or in the past.")


def image_upload(instance, filename):
    imagename , extension = filename.split(".")
    return "screen/%s.%s"%(instance.id,extension)



class Prescription(models.Model):
            
    # id = models.UUIDField(primary_key=True,unique=True,editable=False)
    patient= models.ForeignKey('accounts.Patient', related_name='patient_id', on_delete=models.CASCADE)
    doctor = models.ForeignKey('accounts.Doctor', related_name='doctor_id', on_delete=models.PROTECT)
    day_created = models.DateField(default=datetime.now)
    next_consultation = models.DateField(_("next consultation"))
    clinical =models.ForeignKey('Clinical', related_name='Clinical', on_delete=models.CASCADE)
    cancelation_date= models.DateField(null = True)
    # is_patient_cancels= models.BooleanField(default=False)
    # drug =models.ForeignKey("Drug", on_delete=models.CASCADE)
    # Screen =models.ForeignKey('Screen', on_delete=models.CASCADE)
    
    def isCanceled(self):
        today = date.today()
        method = int((today- self.next_consultation).days)
        if method >=0:
            self.cancel()

    # def my_custom_sql(self):
    #     with connection.cursor() as cursor:
    #         cursor.execute("UPDATE prescription_prescription SET cancelation_date = %s WHERE id = %s", [self.next_consultation, self.id])
    def cancel(self):
        p=Prescription.objects.get(id= self.id)
        p.cancelation_date=self.next_consultation
        p.save()
            
    class Meta:
        verbose_name = 'Prescription'
        verbose_name_plural = 'Prescriptions'
        
        
class active_Ingredient (models.Model):
    name=models.CharField(("Ingredient name"), max_length=100)

    def __str__(self):
        return self.name

class Interaction_status(models.Model):
    typ=models.CharField(max_length=50)

class ingredient_interaction (models.Model):
    first=models.ForeignKey(active_Ingredient,related_name='firstID',verbose_name=("First Active Ingredient "),on_delete=models.CASCADE)
    second=models.ForeignKey(active_Ingredient,verbose_name=("Second Active Ingredient "), related_name='secondID',on_delete=models.CASCADE)
    description =models.TextField(("Description"),max_length=1000)
    status = models.ForeignKey(Interaction_status, on_delete=models.CASCADE)

class StandardDrugs(models.Model):
    name=models.CharField(("Drug name"), max_length=100)
    desease=models.CharField(("Desease name"), max_length=100)
    sideEffects=models.TextField(("Side Effects"),max_length=1000)
    description=models.TextField(("Description"),max_length=1000)
    drugType=models.CharField(("Drug Type"),max_length=100 ,null=True)
    activeIngredient=models.ForeignKey(active_Ingredient , on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name 
    
        
class Drug (models.Model):
    drug = models.ForeignKey(StandardDrugs, related_name='StandardDrugs', on_delete=models.PROTECT)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    start_in = models.DateField(_("Start in"),default=datetime.now)
    end_in = models.DateField(_("End in"))
    dose_per_hour = models.FloatField(_("dose"))
    
    def __str__(self):
        return self.drug.name


class Clinical (models.Model):
    clinical_name =models.CharField(_("Clinical name"), max_length=100)
    clinical_location = models.CharField(_("Clinical location"), max_length=255)
    telephone = models.CharField(max_length=12,null=True)
    phone= models.CharField(max_length=12,null=True)
    doctor= models.ForeignKey(Doctor, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Clinical'
        verbose_name_plural = 'Clinicals'
        
    def __str__(self):
        return self.clinical_name


class StandardScreens(models.Model):
    name = models.CharField(_("screen name"), max_length=100)
    description = models.TextField(_("description"))
    
    def __str__(self):
        return self.name
    
    
class Screen (models.Model):
    screen = models.ForeignKey('StandardScreens', related_name='StandardScreens', on_delete=models.PROTECT)
    image = models.TextField(null=True)
    prescription = models.ForeignKey("Prescription", on_delete=models.CASCADE)
    patient =models.ForeignKey(Patient, on_delete=models.CASCADE)
    deadline= models.DateField()
    is_done = models.BooleanField(default=False)
    
    def __str__(self):
        return self.screen.name
class TestScreen(models.Model):
    image = models.BinaryField(blank=True)
    new = models.ImageField( upload_to=image_upload,null=True,blank=True)
    file= models.FileField(upload_to=image_upload,blank=True)
    file_path= models.FilePathField(blank=True)
    text = models.TextField()

class StandardMedicalAnalysis(models.Model):
    name = models.CharField(_("Medical Analysis"), max_length=100)
    description = models.TextField(_("description"))
    
    def __str__(self):
        return self.name

class MedicalAnalysis(models.Model):
    standard_medical_analysis = models.ForeignKey(StandardMedicalAnalysis,  on_delete=models.CASCADE)
    image = models.TextField(null= True)
    prescription = models.ForeignKey("Prescription", on_delete=models.CASCADE)
    patient =models.ForeignKey(Patient, on_delete=models.CASCADE)
    deadline= models.DateField()
    is_done = models.BooleanField(default=False)
    
    def __str__(self):
        return self.standard_medical_analysis.name
    
class Booking(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    clinical  = models.ForeignKey(Clinical,on_delete=models.CASCADE)
    date = models.DateField(validators= [future_date_validator])
    start = models.TimeField()
    end = models.TimeField()
    allowed_number = models.PositiveSmallIntegerField()
    
    def numberOfPatients(self):
        num = PatientBooking.objects.filter(booking=self).aggregate(Count('id'))['id__count']
        return num
    
    def __str__(self):
        return f"{self.date.strftime('%A')}  {self.date} ({self.start.strftime('%I:%M %p')})"

class PatientBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    patient= models.OneToOneField(Patient,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.booking.date.strftime('%A')}  {self.booking.date} ({self.booking.start.strftime('%I:%M %p')})"

    # def save(self, *args, **kwargs):
    #     if self.text:
    #         # Convert the image to a base64-encoded string
    #         with open(self.text.path, 'rb') as f:
    #             encoded_string = base64.b64encode(f.read()).decode('utf-8')
    #         self.text = encoded_string

    #     super(TestScreen, self).save(*args, **kwargs)
    
# class ClinicalPrescription(models.Model):
#     prescription=models.ForeignKey("Prescription",related_name='Prescription_id', on_delete=models.CASCADE)
#     clinical =models.ForeignKey("Clinical", related_name='Clinical_id', on_delete=models.CASCADE)