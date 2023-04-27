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
def phoneValidate(value):
    numbers ='0123456789'
    if len(value) == 11:
        if value[0]=='0' and value[1]=='1' and (value[2]=='0' or value[2]=='1' or value[2]=='2' or value[2]=='5'):
            for i in value:
                if i not in numbers:
                    raise ValidationError(
                        _('%(value)s is not a valid phone number'),
                        params={'value': value},
                    )
        else:
            raise ValidationError(
                        _('%(value)s is not valid a phone number'),
                        params={'value': value},
                    )
    else:
            raise ValidationError(
                        _('%(value)s length is not 11 numbers.'),
                        params={'value': value},
                    )
        


def future_date_validator(value):
    if date.today() > value:
        raise ValidationError("Date cannot be in the past.")


def image_upload(instance, filename):
    imagename , extension = filename.split(".")
    return "screen/%s.%s"%(instance.id,extension)



class Prescription(models.Model):
            
    # id = models.UUIDField(primary_key=True,unique=True,editable=False)
    patient= models.ForeignKey('accounts.Patient', related_name='patient_id', on_delete=models.CASCADE)
    doctor = models.ForeignKey('accounts.Doctor', related_name='doctor_id', on_delete=models.PROTECT)
    day_created = models.DateField(default=datetime.now)
    next_consultation = models.DateField(_("next consultation"),validators=[future_date_validator])
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
    id = models.IntegerField(primary_key=True, db_index=True, unique=True)
    name=models.CharField(("Ingredient name"), max_length=100)
    if_interaction_exist= models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Interaction_status(models.Model):
    typ=models.CharField(max_length=50)

class ingredient_interaction (models.Model):
    first=models.ForeignKey(active_Ingredient,related_name='firstID',verbose_name=("First Active Ingredient "),on_delete=models.CASCADE)
    second=models.ForeignKey(active_Ingredient,verbose_name=("Second Active Ingredient "), related_name='secondID',on_delete=models.CASCADE)
    description =models.TextField(("Description"),max_length=5000, null=True, blank=True)
    status = models.ForeignKey(Interaction_status, on_delete=models.CASCADE,null=True,blank=True)

class StandardDrugs(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True, unique=True)
    name=models.CharField(("Drug name"), max_length=100,db_index=True, unique= True)
    sideEffects=models.TextField(("Side Effects"),max_length=1000, null=True, blank=True)
    uses=models.TextField(("uses"),max_length=3000, null=True, blank=True)
    warnings=models.TextField(("warnings"),max_length=3000, null=True, blank=True)
    before_taking=models.TextField(("before_taking"),max_length=3000, null=True, blank=True)
    how_to_take=models.TextField(("how_to_take"),max_length=3000, null=True, blank=True)
    miss_dose=models.TextField(("miss_dose"),max_length=3000, null=True, blank=True)
    overdose=models.TextField(("overdose"),max_length=3000, null=True, blank=True)
    what_to_avoid=models.TextField(("what_to_avoid"),max_length=3000, null=True, blank=True)
    activeIngredient=models.ForeignKey(active_Ingredient , on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name 


class Drug (models.Model):
    drug = models.ForeignKey(StandardDrugs, related_name='StandardDrugs', on_delete=models.PROTECT, null=True, blank=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    start_in = models.DateField(_("Start in"),default=datetime.now)
    end_in = models.DateField(_("End in"),validators=[future_date_validator])
    consentration=models.PositiveSmallIntegerField()
    dose_per_hour = models.FloatField(_("dose"))
    drugType=models.CharField(("Drug Type"),max_length=100 ,null=True, blank=True)
    name_if_doesnt_exist= models.CharField(max_length=100,null=True, blank=True)
    
    def __str__(self):
        return self.drug.name


class Clinical (models.Model):
    clinical_name =models.CharField(_("Clinical name"), max_length=100)
    clinical_location = models.CharField(_("Clinical location"), max_length=255)
    telephone = models.CharField(max_length=11,null=True,blank=True,validators=([phoneValidate]))
    phone= models.CharField(max_length=11,validators=([phoneValidate]))
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
    
    def getDayOfWeek(self):
        obj = Booking.objects.get(id=self.id)
        return obj.date.strftime('%A')
    
    def getDayOfWeekAsNumber(self):
        obj = Booking.objects.get(id=self.id)
        day = [7, 1, 2, 3, 4, 5, 6]  # List of integer values for each day of the week, starting with Monday = 2
        day_of_week = day[obj.date.weekday()]  # Get the day of the week as an integer
        return day_of_week
    
    def getStartTwelveMode(self):
        obj=Booking.objects.get(id=self.id)
        return obj.start.strftime('%I:%M %p')
    
    def getEndTwelveMode(self):
        obj=Booking.objects.get(id=self.id)
        return obj.end.strftime('%I:%M %p')
    
    
    def numberOfPatients(self):
        num = PatientBooking.objects.filter(booking=self).aggregate(Count('id'))['id__count']
        return num
    
    def __str__(self):
        return f"{self.date.strftime('%A')}  {self.date} ({self.start.strftime('%I:%M %p')})"

class PatientBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    patient= models.OneToOneField(Patient,on_delete=models.CASCADE)
    class Meta:
        unique_together =(('booking','patient'),)
        index_together =(('booking','patient'),)
    
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
