from django.forms import ValidationError
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework import generics , status, filters ,viewsets
from rest_framework.permissions import IsAuthenticated  
from .permissions import IsDoctor , IsPatient
from django.core import serializers
import base64
import os
from django.core.files import File 
import json
from rest_framework.decorators import action, parser_classes
from rest_framework.fields import CurrentUserDefault
from rest_framework import parsers
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
import base64
from io import StringIO
from base64 import b64decode
from django.core.files.base import ContentFile  
from datetime import date , timedelta
from django.core.cache import cache


class MakePrescription(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = MakePrescriptionSerializer2
    @action (methods=['POST'],detail=True)
    def makeNewPrescriptopn(self,request, pk =None):
        prescription=Prescription.objects.create(
            patient = Patient.objects.get(id = pk),
            doctor = Doctor.objects.get(id=request.user.id),
            clinical = request.data['clinical'],
            next_consultation=request.data['next_consultation']
        )

        



# Create your views here.

# class MakePrescription(generics.ListCreateAPIView):
#     queryset = Prescription.objects.all()
#     serializer_class = ExampleSerializer2
#     # permission_classes = [IsDoctor,]

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         doc = Doctor.objects.get(id=request.user.id)
#         c=list (Clinical.objects.filter(doctor_id= doc.id))
#         def returnID(c):
#             ls=[]
#             for obj in c:
#                 ls.append(obj.id)
#             return(ls)
#         cl = request.data['doctor_clinical']
#         print(cl)
#         print (returnID(c))
#         if  (cl not in returnID(c)):
#             return Response( {'clinical':['clinical does not exist.']},status=status.HTTP_400_BAD_REQUEST)
#             # serializer.validate_data['doctor']= Doctor.objects.get(username=request.user)
#             # serializer.object.doctor = Doctor.objects.get(username=request.user)
#         prescription=serializer.save()
#         return Response({
#             "prescription": MakePrescriptionSerializer(prescription, context=self.get_serializer_context()).data
#             })
    
# class SetDrug(generics.CreateAPIView):
#     permission_classes = [IsDoctor,]
#     authentication_classes = [TokenAuthentication,]
#     serializer_class =  SetDrugSerializer
#     def post(self, request,prescription):
#         serializer = self.serializer_class(data = request.data)
#         if  serializer.is_valid():
#             drug = Drug.objects.create(
#                 drug = serializer.validated_data['drug'],
#                 prescription = prescription,
#                 # start_in= serializer.validated_data['start_in'],
#                 end_in = serializer.validated_data['end_in'],
#                 dose_per_hour= serializer.validated_data['dose_per_hour']
#                 )
#             drug.save()
#             return Response(status=status.HTTP_201_CREATED)
            
#         else :
#             return 0
            
        
# class SetPrescription_(generics.CreateAPIView):
#     permission_classes = [IsDoctor,]
#     authentication_classes = [TokenAuthentication,]
#     serializer_class = SetPrescriptionSerializer
#     def post(self, request, patient_id,):
#         serializer = self.serializer_class(data=request.data)
#         doctor = Doctor.objects.get(id = request.user.id)
#         patient = Patient.objects.get(id= patient_id)
#         serializer.is_valid(raise_exception= True)
#         prescription= Prescription.objects.create(
#             doctor =doctor,
#             patient =patient,
#             clinical = serializer.validated_data['clinical'],
#             next_consultation = serializer.validated_data['next_consultation']
#         )
#         s = SetDrug()
#         # prescription.save()
#         temp=s.post(request= request,prescription=prescription)
#         if temp == 0:
#             prescription.delete()
#             return Response({"message":"please add one drug at least"},status=status.HTTP_400_BAD_REQUEST)
#         else :
#         # json_prescription=serializers.serialize("json",prescription)
#             return Response({"prescription_id":prescription.id},status=status.HTTP_201_CREATED)



class GetCurentClinicalForPatient(generics.ListAPIView):
    permission_classes = [IsDoctor,]
    authentication_classes = [TokenAuthentication,]
    serializer_class = GetCurentClinicalForPatientSerializer
    def get (self, request):
        doctor = Doctor.objects.get(id = request.user.id)
        try:
            clinicals = Clinical.objects.filter(doctor = doctor)
        except Clinical.DoesNotExist:
            return Response({"status":False,"data":None,"message":"No Clinicals yet."},status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(clinicals,many = True)
        return Response({"status":True,"data":serializer.data,"message":"OK"},status=status.HTTP_200_OK)

class GetAllStandardDrugsName(generics.ListAPIView):
    permission_classes=[IsDoctor,]
    authentication_classes = [TokenAuthentication,]
    serializer_class = GetAllStandardDrugsNameSerializer
    def get(self, request):
        try:
            standard_drugs=StandardDrugs.objects.all().values_list('name', flat=True)
            
            return Response({"status":True,"data":self.cache(standard_drugs),"message":"Ok"},status=status.HTTP_200_OK)
        except StandardDrugs.DoesNotExist:
            return Response({"status":False,"data":None,"message":"No Drugs in the system yet"},status=status.HTTP_200_OK)
    def cache(self,standard_drugs):
        data = cache.get('standard_drugs')
        if data is None:
            data = standard_drugs
            cache.set('standard_drugs',data,timeout =3600)
        return standard_drugs

class GetAllStandardDrugsNameFilter(generics.CreateAPIView):
    permission_classes=[IsDoctor,]
    authentication_classes = [TokenAuthentication,]
    def post(self, request):
        word = request.data['word']
        standard_drugs=StandardDrugs.objects.filter(name__startswith=word).values_list('name', flat=True)
        return Response({"status":True,"data":standard_drugs,"message":"Ok"},status=status.HTTP_200_OK)

class SetPrescription(generics.CreateAPIView):
    permission_classes = [IsDoctor,]
    authentication_classes = [TokenAuthentication,]
    serializer_class = SetPrescriptionSerializer
    def post(self, request, patient_id,):
        serializer =self.serializer_class(data=request.data)
        # drug_serializer = self.serializer_class(data=request.data['drug'])
        doctor = Doctor.objects.get(id = request.user.id)
        try:
            patient = Patient.objects.get(id= patient_id)
        except Patient.DoesNotExist:
            return Response({"message":"No patient with this id."},status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception= True)
        drugs= serializer.validated_data.pop('drugs')
        screens = serializer.validated_data.pop('screens')
        medical_analysis = serializer.validated_data.pop('medical_analysis')
        if not (drugs or screens or medical_analysis):
            return Response({"message":"add one drug or one screen or one medical analysis at least."},status=status.HTTP_400_BAD_REQUEST)
        # prescription_serializer = serializer.validated_data.pop('prescription')
        # prescription_serializer.is_valid(raise_exception= True)
        prescription= Prescription.objects.create(
            doctor =doctor,
            patient =patient,
            clinical = serializer.validated_data['clinical'],
            next_consultation = serializer.validated_data['next_consultation']
            )
        
        for drug in drugs:
            try:
                _drug = StandardDrugs.objects.get(name=drug['drug_name'])
            except StandardDrugs.DoesNotExist:
                return Response({"status":False,
                                 "data":None,
                                 "message":"No Drug with this name"},
                                status=status.HTTP_404_NOT_FOUND)
            Drug.objects.create(
                prescription = prescription,
                # **drug
                drug = _drug,
                end_in = drug['end_in'],
                dose_per_hour = drug['dose_per_hour']
                )
        for screen in screens:
            Screen.objects.create(
                prescription = prescription,
                patient = Patient.objects.get(id= patient_id),
                **screen
                )
        for m in medical_analysis:
            MedicalAnalysis.objects.create(
                prescription = prescription,
                patient = Patient.objects.get(id= patient_id),
                **m
                )
        
        # prescription.save()
        # json_prescription=serializers.serialize("json",prescription)
        return Response(status=status.HTTP_201_CREATED)


        
# @api_view(['GET','POST'])
# def makePrescription(request):
#     if request.method == 'GET':
#         prescription = Prescription.objects.all()
#         serializer=serializers.serialize("json",prescription)
#         return JsonResponse(json.loads(serializer),safe=False) 
    
#     elif request.method == 'POST':
#         serializer = MakePrescriptionSerializer(data= request.data)
#         # if MakePrescriptionSerializer.is_valid():
#         doctor = Doctor.objects.get(id = request.user.id)
#         patient = Patient.objects.get(id = request.data['patient'])
#         clinical=request.data['clinical']
#         next_consultation = request.data['next_consultation']
#         doctor_clinicals =list (Clinical.objects.filter(doctor=doctor.id))
#         def returnID(doctor_clinicals):
#             ls=[]
#             for obj in doctor_clinicals:
#                 ls.append(obj.id)
#             return(ls)
#         if (clinical not in returnID(doctor_clinicals)):
#             return Response( {'clinical':['clinical does not exist.']},status=status.HTTP_400_BAD_REQUEST)
#         # prescription = Prescription(
#         #     patient= patient,
#         #     doctor= doctor,
#         #     clinical= Clinical.objects.get(id=clinical),
#         #     next_consultation=next_consultation,
#         # )
#         p=Prescription.objects.create(patient= patient,doctor= doctor,clinical= Clinical.objects.get(id=clinical),next_consultation=next_consultation,)
#         # prescription.save()
#         prescription= Prescription.objects.filter(id = p.id)
#         data = serializers.serialize("json",prescription)
#         return Response(json.loads(data))
    
# @api_view(['POST'])
# def GetMyOldPrescriptions(request):
#     if request.method =='POST':
#         serializer = GetOldPrescriptions(data=request.data) 
#         serializer.is_valid(raise_exception=True)
#         id= serializer.validated_data['id']
#         try:
#             patient= Patient.objects.get(id = id)
#         except Patient.DoesNotExist:
#             return Response({"message":"patient not found"},status=status.HTTP_404_NOT_FOUND)
#         try:
#             old_prescription= Prescription.objects.filter(patient = patient.id)
#         except Prescription.DoesNotExist:
#             return Response({"message":"patient have not prescriptions yet."})
#         serializer=serializers.serialize("json",old_prescription)
#         return Response(json.loads(serializer))
        
        
        
@api_view(['GET','POST'])        
# @permission_classes([IsPatient,])
def postScreen(request ,format=None):
    try:
        # patient = Patient.objects.get(id = request.user.id) ## ده المريض اللي المفروض يشوف اشاعاته
        my_screens = TestScreen.objects.all()## ودول الاشاعات بتوعه كلهم جبتهم بالايدي
        serializer = PostScreenSerializer(my_screens,many =True) ## والسطر ده معناه الداتا اللي راجعة اذا كانت بوست او جيت
    except Patient.DoesNotExist:
        return Response({'message':['Does not exists']},status= status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return Response(serializer.data)
    
    elif request.method == 'POST':
        new_screen = PostScreenSerializer(data= request.data)
        if (new_screen.is_valid()):
            
            # new_screen.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED) # هنا لو الداتا مفهاش مشكلة هيحفظها ويبعتلك ريكويست 201

    
class PostScreen(generics.CreateAPIView):
    serializer_class= PostScreenSerializer
    parser_classes = (parsers.JSONParser)
    # queryset= TestScreen.objects.all()

    def post(self, request, filename, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image= serializer.validated_data['new']
        new_screen= TestScreen.objects.create(new = image)
        return Response({
        "image": PostScreenSerializer(new_screen, context=self.get_serializer_context()).data
        # "token": AuthToken.objects.create(user)[1]
        })
        # imgstr64 = serializer.validated_data['image']
        # imgdata = base64.b64decode(imgstr64)
        # fname = '/tmp/%s.jpg'%(str(screen.id))
        # with open(fname,'wb') as f:
        #     f.write(imgdata)
        # imgname = '%s.jpg'%(str(image.id))
        # myphoto.image.save(imgname,File(open(fname,'r')))
        # os.remove(fname)
        # return Response(new_screen.data,status= status.HTTP_400_BAD_REQUEST)
        
        
        
        
class UserUploadedPicture(APIView):
    
    # parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    serializer_class =PostScreenSerializer
    def post(self,request, format=None):

        serializer = self.serializer_class(data= request.FILES)
        # # image= request.data['new']
        # # file= request.data['file']
        # # file_path= request.data['file_path']
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # image = request.data['new']
        # new_screen= TestScreen.objects.create(new = image)
        # new_screen.save()
        return Response(status=status.HTTP_200_OK)

    
    def get(self,request):
        obj = TestScreen.objects.all()
        serializer = PostScreenSerializer(obj,many= True)
        # serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
    
# @api_view(['POST'])  
# # @parser_classes([JSONParser,parsers.MultiPartParser, parsers.FormParser])
# def UserUploadedPicture(request):
#     if request.method == 'POST' :
        
#         image = request.FILES['text']
#         # imgstr = image.readlines()

#         data = ContentFile(base64.b64decode(image))
#         format,imgstr = data.split(';base64,')
#         print("format", format)
#         ext = format.split('/')[-1]
#         file_name = "'myphoto." + ext
#         TestScreen.text.save(file_name, imgstr, save = True)
#         # image_base64 = image.split('base64', 1 )
#         # img_data = base64.b64decode(image)
#         # image_base64 = img_data.split('base64,', 1 )
#         # new_screen= TestScreen.objects.create(new = image)
#         # new_screen.save()
#         # img_buffer = StringIO()
#         # image.save(img_buffer, format="image")
#         # img_str = base64.b64encode(img_buffer.getvalue())
#         # TestScreen.objects.create(text = img_data)
#         # TestScreen.save()
        
#         return Response(status=status.HTTP_200_OK)
    
@api_view(['POST'])    
def UserUploadedPicture(request):
    if request.method == 'POST' and request.FILES['new']:
        image = request.FILES['new']
        new_screen= TestScreen.objects.create(new = image)
        new_screen.save()
        return Response(status=status.HTTP_200_OK)
    

@api_view(['POST'])
def upload_image(request):
    try:
        image = request.data['new']
    except Exception as e:
        return JsonResponse(ValidationError(_('not a valid SAMLRequest: {}').format(repr(e))))  

    # encoded_string = base64.b64encode(image.read()).decode('utf-8')
    format,imgstr = image.split(';base64,')
    
    obj= TestScreen.objects.create(text = imgstr)
    obj.save()

    return Response( status=status.HTTP_201_CREATED)

class GetScreen(generics.ListAPIView):
    # queryset = TestScreen.objects.all()
    serializer_class = PostScreenSerializer
    
    def get(self,request):
        screen = TestScreen.objects.get(id = 26)
        serializer = self.serializer_class(screen,many = False)
        return Response(serializer.data,status=status.HTTP_200_OK)
        

class GetActiveDoctorPatients(generics.ListAPIView):
    authentication_classes =[ TokenAuthentication,]
    permission_classes= [IsDoctor,]
    serializer_class =GetPrescriptionDoctorPatientClinicalSerializer
    def get(self,request):
        doctor = Doctor.objects.get(id = request.user.id)
        active_patients= Prescription.objects.filter(doctor = doctor.id, cancelation_date__isnull=True).order_by('-next_consultation')
        if not active_patients :
            return Response({"status":False,"data":None,'message':'Active patients do not exist'})
        unique_patients = []
        unique_ids = set()
        for patient in active_patients:
            if patient.patient.id not in unique_ids:
                unique_patients.append(patient)
                unique_ids.add(patient.patient.id)   
        serializer =self.serializer_class(unique_patients,many = True)        
        return Response({"status":True,
                            "data":serializer.data,
                            "message":"These are active patients"},
                        status=status.HTTP_200_OK)
        
class GetOldDoctorPatients(generics.ListAPIView):
    authentication_classes =[ TokenAuthentication,]
    permission_classes= [IsDoctor,]
    serializer_class =GetPrescriptionDoctorPatientClinicalSerializer
    def get(self,request):
        doctor = Doctor.objects.get(id = request.user.id)
        old_patients= Prescription.objects.filter(doctor = doctor.id, cancelation_date__isnull=False).order_by('-next_consultation')
        if not old_patients :
            return Response({"status":False,"data":None,'message':'Old patients do not exist'})
        unique_patients = []
        unique_ids = set()
        for patient in old_patients:
            if patient.patient.id not in unique_ids:
                unique_patients.append(patient)
                unique_ids.add(patient.patient.id)   
        serializer =self.serializer_class(unique_patients,many = True)
        return Response({"status":True,
                            "data":serializer.data,
                            "message":"These are Old patients"},
                        status=status.HTTP_200_OK)
        
class GetAllDoctorPatients(generics.ListAPIView):
    authentication_classes =[ TokenAuthentication,]
    permission_classes= [IsDoctor,]
    serializer_class =GetPrescriptionDoctorPatientClinicalSerializer
    def get(self,request):
        doctor = Doctor.objects.get(id = request.user.id)
        All_patients= Prescription.objects.filter(doctor = doctor.id)
        if not All_patients :
            return Response({"status":False,"data":None,'message':'All patients do not exist'})
        unique_patients = []
        unique_ids = set()
        for patient in All_patients:
            if patient.patient.id not in unique_ids:
                unique_patients.append(patient)
                unique_ids.add(patient.patient.id)           
        serializer =self.serializer_class(unique_patients,many = True)
        return Response({"status":True,
                            "data":serializer.data,
                            "message":"These are All patients"},
                        status=status.HTTP_200_OK)
        
class GetSpecificDoctorPatientPrescription(generics.ListAPIView):
    authentication_classes =[ TokenAuthentication,]
    permission_classes= [IsDoctor,]
    # serializer_class = GetSpecificPrescriptionDoctorPatientClinicalSerializer
    def get(self, request, p_id):
        prescription=Prescription.objects.get(id = p_id)
        doctor = Doctor.objects.get(id= request.user.id)
        if doctor.id != prescription.doctor.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        patient = Patient.objects.get(id = prescription.patient.id)
        clinical = Clinical.objects.get (id =prescription.clinical.id)
        drugs = Drug.objects.filter(prescription=prescription.id)
        screens= Screen.objects.filter(prescription=prescription.id)
        medical_analysis = MedicalAnalysis.objects.filter(prescription=prescription.id)
        prescription_serializer = GetPrescriptionSerializer(prescription).data
        patient_serializer = GetPatientSerializer(patient).data
        doctor_serializer = GetDoctorSerializer(doctor).data
        clinical_serializer = GetClinicalSerializer(clinical).data
        drugs_serializer = SetDrugSerializer(drugs,many = True).data
        screens_serializer = GetScreenSerialzer (screens, many = True).data
        medical_analysis_serializer = GetMedicalAnalysisSerializer(medical_analysis, many = True).data
        # serializer =self.serializer_class(prescription,many=True)
        serializer  ={"prescription":prescription_serializer,
                      "patient":patient_serializer,
                      "doctor":doctor_serializer,
                      "clinical":clinical_serializer,
                      "drugs":drugs_serializer,
                      "screens":screens_serializer,
                      "medical_analysis":medical_analysis_serializer}
                    
        return Response(serializer,status=status.HTTP_200_OK)
        


class GetMyActivePrescription(generics.ListAPIView):
    permission_classes = [IsPatient,]
    authentication_classes = [TokenAuthentication,]
    # serializer_class = SetPrescriptionSerializer
    def get(self, request):
        patient= Patient.objects.get(id= request.user.id)
        try:
            prescription=Prescription.objects.get(patient = patient,cancelation_date__isnull=True)
        except Prescription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)            
        doctor = Doctor.objects.get(id = prescription.doctor.id)
        clinical = Clinical.objects.get (id =prescription.clinical.id)
        drugs = Drug.objects.filter(prescription=prescription.id)
        screens= Screen.objects.filter(prescription=prescription.id)
        medical_analysis = MedicalAnalysis.objects.filter(prescription=prescription.id)
        prescription_serializer = GetPrescriptionSerializer(prescription).data
        patient_serializer = GetPatientSerializer(patient).data
        doctor_serializer = GetDoctorSerializer(doctor).data
        clinical_serializer = GetClinicalSerializer(clinical).data
        drugs_serializer = SetDrugSerializer(drugs,many = True).data
        screens_serializer = GetScreenSerialzer (screens, many = True).data
        medical_analysis_serializer = GetMedicalAnalysisSerializer(medical_analysis, many = True).data
        # serializer =self.serializer_class(prescription,many=True)
        serializer  ={"prescription":prescription_serializer,
                      "patient":patient_serializer,
                      "doctor":doctor_serializer,
                      "clinical":clinical_serializer,
                      "drugs":drugs_serializer,
                      "screens":screens_serializer,
                      "medical_analysis":medical_analysis_serializer}
                    
        return Response(serializer,status=status.HTTP_200_OK)

class CancelMyPrescription(generics.CreateAPIView):
    permission_classes = [IsPatient,]
    authentication_classes = [TokenAuthentication,]
    serializer_class = CancelMyPrescriptionSerializer
    def post(self,request):
        serializer =self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception= True)
        if serializer.validated_data['is_canceled']==True:
            patient= Patient.objects.get(id= request.user.id)
            prescription=Prescription.objects.get(patient = patient,cancelation_date__isnull=True)
            prescription.cancelation_date = date.today()
            prescription.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class GetMyOldPrescriptions(generics.ListAPIView):
    permission_classes = [IsPatient,]
    authentication_classes = [TokenAuthentication,]
    def get(self, request):
        patient= Patient.objects.get(id= request.user.id)
        try:
            old_prescriptions = Prescription.objects.filter(patient = patient, cancelation_date__isnull=False)
        except Prescription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=[]
        for p in old_prescriptions:
            doctor = Doctor.objects.get(id = p.doctor.id)
            clinical = Clinical.objects.get (id =p.clinical.id)
            prescription_serializer = GetPrescriptionSerializer(p).data
            doctor_serializer = ListPrescriptionsDoctor(doctor).data
            clinical_serializer = ListPrescriptionsClinical(clinical).data
            ser = [{"prescription":prescription_serializer,"doctor":doctor_serializer,"clinical":clinical_serializer}]
            serializer = serializer + ser
        return Response(serializer,status=status.HTTP_200_OK)
    
    
class GetSpecificOldPrescription(generics.ListAPIView):
    permission_classes = [IsPatient,]
    authentication_classes = [TokenAuthentication,]
    def get(self, request,p_id):
        patient= Patient.objects.get(id= request.user.id)
        try:
            old_prescriptions = Prescription.objects.get(id = p_id)
        except Prescription.DoesNotExist:
            return Response({"message":"No prescription with this id"},status=status.HTTP_404_NOT_FOUND)
        if old_prescriptions.patient.id != patient.id :
            return Response({"message":"No prescription with this id"},status=status.HTTP_404_NOT_FOUND)
        doctor = Doctor.objects.get(id = old_prescriptions.doctor.id)
        clinical = Clinical.objects.get (id =old_prescriptions.clinical.id)
        drugs = Drug.objects.filter(prescription=old_prescriptions.id)
        screens= Screen.objects.filter(prescription=old_prescriptions.id)
        medical_analysis = MedicalAnalysis.objects.filter(prescription=old_prescriptions.id)
        prescription_serializer = GetPrescriptionSerializer(old_prescriptions).data
        patient_serializer = GetPatientSerializer(patient).data
        doctor_serializer = GetDoctorSerializer(doctor).data
        clinical_serializer = GetClinicalSerializer(clinical).data
        drugs_serializer = SetDrugSerializer(drugs,many = True).data
        screens_serializer = GetScreenSerialzer (screens, many = True).data
        medical_analysis_serializer = GetMedicalAnalysisSerializer(medical_analysis, many = True).data
        # serializer =self.serializer_class(prescription,many=True)
        serializer  ={"prescription":prescription_serializer,
                      "patient":patient_serializer,
                      "doctor":doctor_serializer,
                      "clinical":clinical_serializer,
                      "drugs":drugs_serializer,
                      "screens":screens_serializer,
                      "medical_analysis":medical_analysis_serializer}
                    
        return Response(serializer,status=status.HTTP_200_OK)
    
    

class SetAppointmentForDoctors(generics.CreateAPIView):
    permission_classes = [IsDoctor,]
    authentication_classes = [TokenAuthentication,]
    serializer_class= BookingSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor = Doctor.objects.get (id = request.user.id)
        doctor_clinicals= Clinical.objects.filter(doctor=doctor)
        id_list = []
        for obj in doctor_clinicals:
            id_list.append(obj.id)
        if serializer.validated_data['clinical'].id not in id_list:
            print(id_list)
            return Response("clinical not found",status=status.HTTP_404_NOT_FOUND)
        clinical = serializer.validated_data['clinical']
        date = serializer.validated_data['date']
        start = serializer.validated_data['start']
        end = serializer.validated_data['end']
        allowed_number = serializer.validated_data['allowed_number']
        Booking.objects.create(
            doctor=doctor,
            clinical=clinical,
            date=date,
            start=start,
            end  =end,
            allowed_number =allowed_number,
        )
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class ModifySpecificAppointmentForDoctor(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsDoctor,]
    authentication_classes = [TokenAuthentication,]
    serializer_class= BookingSerializer
    def get(self, request,id):
        doctor =Doctor.objects.get(id= request.user.id)
        my_appointments = Booking.objects.filter(doctor =doctor)
        id_list = []
        for obj in my_appointments:
            id_list.append(obj.id)
        if id not in id_list:
            return Response("Appointment not dound",status=status.HTTP_404_NOT_FOUND)
        appointment =Booking.objects.get(id=id)
        serializer = self.serializer_class(appointment)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request,id):
        serializer =self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor =Doctor.objects.get(id= request.user.id)
        my_appointments = Booking.objects.filter(doctor =doctor)
        id_list = []
        for obj in my_appointments:
            id_list.append(obj.id)
        if id not in id_list:
            return Response("Appointment not dound",status=status.HTTP_404_NOT_FOUND)
        appointment =Booking.objects.get(id=id)
        clinical = serializer.validated_data['clinical']
        date = serializer.validated_data['date']
        start = serializer.validated_data['start']
        end = serializer.validated_data['end']
        allowed_number = serializer.validated_data['allowed_number']
        appointment.clinical=clinical
        appointment.date=date
        appointment.start=start
        appointment.start=start
        appointment.end=end
        appointment.allowed_number=allowed_number
        appointment.save()
        # serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self, request,id):
        doctor =Doctor.objects.get(id= request.user.id)
        my_appointments = Booking.objects.filter(doctor =doctor)
        id_list = []
        for obj in my_appointments:
            id_list.append(obj.id)
        if id not in id_list:
            return Response("Appointment not dound",status=status.HTTP_404_NOT_FOUND)
        appointment =Booking.objects.get(id=id)
        appointment.delete()
        return Response("appointment has been deleted",status=status.HTTP_200_OK)
    
class GetMyAllAppointmentsForDoctor(generics.ListAPIView):
    permission_classes = [IsDoctor,]
    authentication_classes = [TokenAuthentication,]
    serializer_class= BookingSerializer
    def get(self, request):
        doctor = Doctor.objects.get(id = request.user.id)
        my_all_appointments = Booking.objects.filter(doctor=doctor)
        serializer = self.serializer_class(my_all_appointments,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
        
# api_view(['GET','POST'])
# def makePrescription(request):
#     if request.method == 'GET':
#         prescription = Prescription.objects.all()
#         screen= Screen.objects.all()
#         serializer=serializers.serialize("json",prescription)
#         return JsonResponse(json.loads(serializer),safe=False) 
       
#     elif request.method == 'POST':
#         serializer =CreatePrescriptionSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         prescription = serializer.save()
#         return Response({'Prescription':prescription.data},status=status.HTTP_201_CREATED)


#get certain patient prescriptions 
# @api_view(['GET'])
# def CPPviews(request):
#      prescriptions = prescription.objects.filter(
#      patientID = request.data['patientID']
#      )
#      serializer = prescriptionSerializer(prescriptions, many=True)
#      return Response(serializer.data)

            
        
# # def some_view(request):
#     doc = Doctor.objects.get(id= request.user.id)
#     clinical = Clinical.objects.filter(doctor=doc).first()
#     patient = Patient.objects.all()
#     # qs = Prescription.objects.filter(clinical =clinical)
#     serialized_obj = serializers.serialize ('python', doc.first_name)
#     return JsonResponse(serialized_obj, safe=False)

# class Presrializer:
#     def __init__(self, patient, clinical, next_consultation):
#         self.doctor = Doctor.objects.get(id=self.context['request'].user.id)
#         clinicals = Clinical.objects.filter(doctor__id=self.doctor.id)
#         self.patient = patient
#         self.clinical = clinical
#         self.next_consultation = next_consultation
        
# def serializePrescription(Presrializer):
#         return {
#     'doctor': Presrializer.doctor,
#     'patient': Presrializer.patient,
#     'clinical': Presrializer.clinical,
#     'next_consultation': Presrializer.next_consultation
# }
        
# def deserialize_order(prescription_data):
#     return Prescription(
#         doctor=prescription_data['doctor'],
#         patient=prescription_data['patient'],
#         clinical=prescription_data['clinical'],
#         next_consultation=prescription_data['next_consultation'],
#     )

# @api_view(['POST'])
# # @authentication_classes([TokenAuthentication])
# def MakePrescription(request):

#     if request.method == 'POST':
#         doc = Doctor.objects.get(id=request.user.id)
#         c=Clinical.objects.filter(doctor__id= doc.id).first()
#         prescription= Prescription.objects.filter(clinical =c)
#         all_prescription= MakePrescriptionSerializer(prescription, many=True)
#         prescription_data =MakePrescriptionSerializer(data= request.data)
#         if (prescription_data.is_valid()):
#             prescription_data.save()
#             return Response(all_prescription.data,status= status.HTTP_201_CREATED)
#         return Response(prescription_data.data,status= status.HTTP_400_BAD_REQUEST)
