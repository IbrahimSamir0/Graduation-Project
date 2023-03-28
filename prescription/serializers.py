from rest_framework import  serializers
# from accounts.serializers impo
from .models import *
from accounts.models import User,Doctor , Patient
from rest_framework.response import Response
from rest_framework import generics , status, filters ,viewsets
from django.http.response import JsonResponse
from rest_framework.fields import CurrentUserDefault

# class Clinicals(serializers.Serializer):
#     clinicall = serializers.ChoiceField(choices=[Clinical.objects.get(doctor = 9)])    



# def get_doc(self):
#         return Doctor.objects.get(id=self.context['request'].uesr.id)

# class ClinicalSerializer():
#     def __init__(self,id):
#         self.clinical = Clinical.objects.filter(doctor_id = id)
#         self.id = 

class GetPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['first_name','last_name','get_age','gender']
        
class SetPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id']

class GetDoctorSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['first_name','last_name','bio']
        
class SetDoctorSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id']

class GetClinicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinical
        fields = ['clinical_name','clinical_location','telephone','phone']
        
class SetClinicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinical
        fields = ['clinical_name','clinical_location','telephone','phone','doctor']
        
class SetClinicalForPrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinical
        fields = ['clinical_name']
        
class GetPrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id','day_created','next_consultation']
        
class GetDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields= ['first_name','last_name','bio']
        
class GetPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields =['id','first_name','last_name','get_age','gender']
        
class SetDrugSerializer(serializers.ModelSerializer):
    # prescription=SetPrescriptionSerializer()
    drug_name = serializers.CharField()
    class Meta:
        model = Drug
        fields = ['drug_name','end_in','dose_per_hour']

class GetAllStandardDrugsNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandardDrugs
        fields=['name']

class GetScreenSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ['screen','deadline','image']
        
class SetScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields =['screen','deadline']
        
class SetMedicalAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalAnalysis
        fields =['standard_medical_analysis','deadline']
        
class GetMedicalAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalAnalysis
        fields =['standard_medical_analysis','deadline','image']
        
class SetPrescriptionSerializer(serializers.ModelSerializer):
    drugs= SetDrugSerializer(many = True)
    screens = SetScreenSerializer(many = True)
    medical_analysis =SetMedicalAnalysisSerializer(many = True)
    class Meta:
        model = Prescription
        fields = ['clinical','next_consultation','drugs','screens','medical_analysis']
        

class ListPrescriptionsDoctor(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields=['first_name','last_name']
        
class ListPrescriptionsClinical(serializers.ModelSerializer):
    class Meta:
        model = Clinical
        fields=['clinical_name','clinical_location']


# class SetPrescriptionSerializer(serializers.Serializer):
#     clinical=SetClinicalForPrescriptionSerializer()
#     next_consultation=GetPrescriptionSerializer()
    
#     class Meta:
#         fields = ('clinical','next_consultation')
        
        
class MakePrescriptionSerializer2(serializers.Serializer):
    def _user(self, obj):
        print(self.context['request'].user.id)
        print(CurrentUserDefault()) 
        return (self.context['request'].user)

    next_consultation= serializers.DateField()    
    # clinical=serializers.IntegerField()
    # user = Doctor.objects.get(username=username)
    # owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # # user = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # user=serializers.SerializerMethodField('_user')
    # doctor=Doctor.objects.get(id = CurrentUserDefault())
    # print(user)
    clinical = serializers.PrimaryKeyRelatedField(queryset=Clinical.objects.filter(doctor__username='doctor'))
    

    
    class Meta:
        fields = ('clinical','next_consultation',)
        
        
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id','clinical','date','start','end','allowed_number']
        
        
# class ExampleSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Clinical.objects.filter(doctor=2)
#         fields = '__all__'
        
# class ExampleSerializer2(serializers.ModelSerializer):
#     clinical= ExampleSerializer
#     class Meta:
#         model = Prescription
#         fields = '__all__'
#         expect = 'clinical'
    
    # c= Clinicals()
    # def __init__(self,d_id):
    #     self.clinical = Clinical.objects.filter(doctor_id = d_id)
    #     self.doctor = Doctor.objects.get(id=d_id)
    #     # self.prescription = Prescription.objects.all()
    #     self.standardDrugs = StandardDrugs.objects.all()
    #     # self.patient = Patient.objects.get(id = p_id)
    #     # self.next_consultation = next_consultation
    # def get_data(self):
    #     return Prescription.objects.all()
        
    # def create(self,validated_data):      
    #     # p=validated_data['patient_num']
    #     # doc = Doctor.objects.get(id=self.context['request'].user.id)
    #     # if validated_data['clinical'] == Clinical.objects.get(doctor=doc):
    #         # c = Clinical.objects.get(doctor=doc)
    #     prescription = Prescription(
    #         # email=validated_data['email'] ,
    #         patient=Patient.objects.get(id=validated_data['patient']),
    #         doctor = Doctor.objects.get(id=self.context['request'].user.id) ,
    #         next_consultation=validated_data['next_consultation'],
    #         clinical=self.clinical,
    #         # typ=doctor_type,
    #         # is_active =False,
    #         # doctor_number=validated_data['doctor_number'],
    #         # password = make_password(validated_data['password'])
    #     )
    #     prescription.save()
    #     return prescription 
        
    # class Meta:
    #     model = Prescription
    #     fields = ('id','clinical','patient','next_consultation')
# class ClinicalSerializer(serializers.ModelSerializer):
#      class Meta:
#         model = Clinical
#         fields = '__all__'

class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = '__all__'
        
        
class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'

class CreatePrescriptionSerializer(serializers.ModelSerializer):
    # doctor_clinical=serializers.PrimaryKeyRelatedField(queryset=Clinical.objects.filter(doctor=2))
    screen = ScreenSerializer
    drug = DrugSerializer
    class Meta:
        model = Prescription
        fields =['id','patient','next_consultation','clinical']
    

    def create(self,validated_data):      
        # p=validated_data['patient_num']
        doc = Doctor.objects.get(id=self.context['request'].user.id)
        # if validated_data['clinical'] == Clinical.objects.get(doctor=doc):
            # c = Clinical.objects.get(doctor=doc)
        prescription = Prescription(
            # email=validated_data['email'] ,
            patient=validated_data['patient'],
            doctor = doc  ,
            next_consultation=validated_data['next_consultation'],
            clinical=validated_data['doctor_clinical'],
            # typ=doctor_type,
            # is_active =False,
            # doctor_number=validated_data['doctor_number'],
            # password = make_password(validated_data['password'])
        )
        prescription.save()
        return prescription 

    # return Response({"message": ["Doesn't match new password."]}, status=status.HTTP_400_BAD_REQUEST)
    

    
class PostScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestScreen
        fields = ['text']
        
        # def create(self,validated_data):
        #     pat = Patient.objects.get(id=self.context['request'].user.id)
            
        #     screen =Screen(
        #         patinet= pat,
        #         image= validated_data['image']
        #     )
class GetScreenSerializer(serializers.ModelSerializer):
    class Meta :
        model = TestScreen
        fields = ['text']

class GetOldPrescriptions(serializers.Serializer):
    id=serializers.IntegerField()
    
    class Meta:
        field = ['id']
        

class GetCurentClinicalForPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinical
        fields = ['id','clinical_name']
        
        
class GetDoctorPAtientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id','first_name','last_name','phone','avatar','city','get_age']
        
        
class GetPrescriptionDoctorPatientClinicalSerializer(serializers.ModelSerializer):
    clinical = GetCurentClinicalForPatientSerializer()
    patient = GetDoctorPAtientSerializer()
    class Meta:
        model= Prescription
        fields =['id','patient','clinical']
        
# class GetSpecificPrescriptionDoctorPatientClinicalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= Prescription
#         fields =['id','patient','clinical']
        
class CancelMyPrescriptionSerializer(serializers.Serializer):
    is_canceled = serializers.BooleanField()
    
    
    
