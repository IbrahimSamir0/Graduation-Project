from django.forms import ValidationError
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics , status
from rest_framework.permissions import IsAuthenticated  
from .permissions import IsDoctor , IsPatient
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from datetime import date ,datetime,timedelta
from django.core.cache import cache
# from .bot.run import RUN
# from .zoz.run import RUN
import threading
from django.db.models import F, Q, OuterRef, Subquery 
from django.core import serializers as ser



# class MakePrescription(viewsets.ModelViewSet):
#     queryset = Prescription.objects.all()
#     serializer_class = MakePrescriptionSerializer2
#     @action (methods=['POST'],detail=True)
#     def makeNewPrescriptopn(self,request, pk =None):
#         prescription=Prescription.objects.create(
#             patient = Patient.objects.get(id = pk),
#             doctor = Doctor.objects.get(id=request.user.id),
#             clinical = request.data['clinical'],
#             next_consultation=request.data['next_consultation']
#         )

        



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
        return Response({"status":True,"data":serializer.data,"message":"successful"},status=status.HTTP_200_OK)

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

class GetAllStandardDrugsNameFilter(generics.ListAPIView):
    permission_classes=[IsDoctor,]
    authentication_classes = [TokenAuthentication,]
    def get(self, request, format=None):
        query = request.GET.get('q', '')
        # word = request.data['word']
        standard_drugs=StandardDrugs.objects.filter(name__istartswith=query).values_list('name', flat=True)
        results = [str(obj) for obj in standard_drugs]
        return Response({"status":True,"data":results,"message":"successful"},status=status.HTTP_200_OK)

class SetPrescription(generics.CreateAPIView):
    permission_classes = [IsDoctor,]
    authentication_classes = [TokenAuthentication,]
    serializer_class = SetPrescriptionSerializer
        
    def run(self,doctor,patient,patient_id,serializer,drugs,screens,medical_analysis):
        try:
            cancel_prescription=Prescription.objects.get(patient=patient,cancelation_date__isnull=True)
            cancel_prescription.cancelation_date = date.today()
            cancel_prescription.save()
        except Prescription.DoesNotExist:
            pass
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
                pass
                # run = RUN()
                # run.open()
                # err_list =run.prepare_drugs([drug['drug_name']])
                # if not err_list:
                #     _drug = StandardDrugs.objects.get(name=drug['drug_name'])
                # else:
                #     _drug= None
            if _drug is not None:
                new_drug=Drug.objects.create(
                    prescription = prescription,
                    # **drug
                    consentration = drug['consentration'],
                    drug = _drug,
                    end_in = drug['end_in'],
                    dose_per_hour = drug['dose_per_hour']
                    )
                time_difference = datetime.combine(drug['end_in'], timezone.now().time()) - datetime.combine(timezone.now().date(), timezone.now().time())
                difference_in_hours = int(time_difference.total_seconds() / 3600)
                num_of_times=int(difference_in_hours/drug['dose_per_hour'])
                current_time =timezone.now()
                
                for _ in range(num_of_times):
                # if current_time <= drug['end_in']:
                    current_time += timedelta(hours=drug['dose_per_hour'])
                    PatientCommitment.objects.create(drug=new_drug, 
                                                    date=current_time
                                                    ,patient=patient)
            else:
                if drug['drug_name'] in err_list:
                    newdrug=Drug.objects.create(
                        prescription = prescription,
                        # **drug
                        consentration = drug['consentration'],
                        name_if_doesnt_exist = drug['drug_name'],
                        end_in = drug['end_in'],
                        dose_per_hour = drug['dose_per_hour']
                        )
                    time_difference = datetime.combine(drug['end_in'], timezone.now().time()) - datetime.combine(timezone.now().date(), timezone.now().time())
                    difference_in_hours = int(time_difference.total_seconds() / 3600)
                    num_of_times=int(difference_in_hours/drug['dose_per_hour'])
                    current_time =timezone.now()
                    
                    for _ in range(num_of_times):
                    # if current_time <= drug['end_in']:
                        current_time += timedelta(hours=drug['dose_per_hour'])
                        PatientCommitment.objects.create(drug=newdrug, 
                                                        date=current_time
                                                        ,patient=patient)
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
        patient_booking=PatientBooking.objects.get(patient=patient,doctor=doctor)
        patient_booking.delete()
        # objs = Prescription.objects.filter(cancelation_date__isnull=True).exclude(id=prescription.id)
        # objs.update(cancelation_date=date.today())


    
    def post(self, request, patient_id,):
        serializer =self.serializer_class(data=request.data)
        # drug_serializer = self.serializer_class(data=request.data['drug'])
        doctor = Doctor.objects.get(id = request.user.id)
        try:
            patient =Patient.objects.get(id= patient_id)
        except Patient.DoesNotExist:
            return Response({"message":"No patient with this id."},status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception= True)
        drugs= serializer.validated_data.pop('drugs')
        screens = serializer.validated_data.pop('screens')
        medical_analysis = serializer.validated_data.pop('medical_analysis')
        if not (drugs or screens or medical_analysis):
            return Response({"message":"add one drug or one screen or one medical analysis at least."},status=status.HTTP_400_BAD_REQUEST)
        thread_1 = threading.Thread(target=self.run, args=(doctor, patient, patient_id, serializer, drugs, screens, medical_analysis))
        thread_1.start()
        return Response({"status":True,
                    "data":None,
                    "message":"Success"},
                    status=status.HTTP_201_CREATED)
            
        # prescription_serializer = serializer.validated_data.pop('prescription')
        # prescription_serializer.is_valid(raise_exception= True)
        
class DrugDeteails(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication,]
    serializer_class = StandatrdDrugNameSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            standard_drug=StandardDrugs.objects.get(name=serializer.validated_data['name'].lower())
            data=DrugDeteailsSerializer(standard_drug, many=False)
            return Response({"status":True,
                    "data":data.data,
                    "message":"Success"},
                    status=status.HTTP_200_OK)
        except StandardDrugs.DoesNotExist:
            return Response({"status":False,
                    "data":{
                            "name":serializer.validated_data['name'],
                            "sideEffects":"Data does not exist.",
                            "uses":"Data does not exist.",
                            "warnings":"Data does not exist.",
                            "before_taking":"Data does not exist.",
                            "how_to_take":"Data does not exist.",
                            "miss_dose":"Data does not exist.",
                            "overdose":"Data does not exist.",
                            "what_to_avoid":"Data does not exist.",
                            "activeIngredient":{"name":"Data does not exist."},
                            },
                    "message":"Success"},
                    status=status.HTTP_200_OK)
            
        

        
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
        
        
class PostScreen(generics.CreateAPIView):
    serializer_class=PostScreenSerializer
    def post(self,request ,format=None):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":True,"data":None,"message":"Sucsess"}, status= status.HTTP_201_CREATED) 
    
class GetMyScreens(generics.ListAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsPatient,]
    serializer_class=GetScreenSerialzer
    def get(self, request):
        patient= Patient.objects.get(id=request.user.id)
        my_screens = Screen.objects.filter(patient=patient).order_by('-id')
        if not my_screens:
            return Response({"status":False,
                             "data":None,
                             "message":"No Screens yet"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer= self.serializer_class(my_screens, many= True)
        return Response({"status":True,
                         "data":serializer.data,"message":"True"},status=status.HTTP_200_OK)
        
class AddOrUpdateScreenForPatient(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsPatient,]
    serializer_class=PostScreenSerializer
    def put(self, request,id):
        screen =Screen.objects.get(id= id)
        serializer= self.serializer_class(screen, data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":True,"data":serializer.data,"message":"Success"},status=status.HTTP_200_OK)
        
        
class GetMySpecificScreens(generics.ListAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsPatient]
    serializer_class=PostScreenSerializer
    def get(self, request, id):
        patient= Patient.objects.get(id= request.user.id)
        try:
            my_screens = Screen.objects.get(id =id,patient=patient)
            serializer= self.serializer_class(my_screens)
            return Response({"status":True,
                         "data":serializer.data,"message":"True"},status=status.HTTP_200_OK)
        except Screen.DoesNotExist:
            return Response({"status":False,
                             "data":None,
                             "message":"No Screens yet"},
                            status=status.HTTP_200_OK)
        
class GetPatientScreens(generics.ListAPIView):
    authentication_classes =[TokenAuthentication,]
    permission_classes = [IsDoctor,]
    serializer_class = PostScreenSerializer
    def get(self,request,id):
        patient = Patient.objects.get(id = id)
        screens = Screen.objects.filter(patient=patient).order_by('-id')
        serializer = self.serializer_class(screens, many= True)
        return Response({"status":True,"data":serializer.data,"message":"Success"},status=status.HTTP_200_OK)

class GetPatientTests(generics.ListAPIView):
    authentication_classes =[TokenAuthentication,]
    permission_classes = [IsDoctor,]
    serializer_class = PostMedicalaAnalysisSerializer
    def get(self,request,id):
        patient = Patient.objects.get(id = id)
        tests = MedicalAnalysis.objects.filter(patient=patient).order_by('-id')
        serializer = self.serializer_class(tests, many= True)
        return Response({"status":True,"data":serializer.data,"message":"Success"},status=status.HTTP_200_OK)


class GetMyMedicalAnlaysis(generics.ListAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsPatient,]
    serializer_class=GetMedicalAnalysisSerializer
    def get(self, request):
        patient= Patient.objects.get(id=request.user.id)
        tests = MedicalAnalysis.objects.filter(patient=patient).order_by('-id')
        if not tests:
            return Response({"status":False,
                             "data":None,
                             "message":"No Screens yet"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer= self.serializer_class(tests, many= True)
        return Response({"status":True,
                         "data":serializer.data,"message":"True"},status=status.HTTP_200_OK)
        
class AddOrUpdateMedicalAnalysisForPatient(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsPatient,]
    serializer_class=PostMedicalaAnalysisSerializer
    def put(self, request,id):
        test =MedicalAnalysis.objects.get(id= id)
        serializer= self.serializer_class(test, data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":True,"data":serializer.data,"message":"Success"},status=status.HTTP_200_OK)
        

class GetPatientMedicalAnalysis(generics.ListAPIView):
    authentication_classes =[TokenAuthentication,]
    permission_classes = [IsDoctor,]
    serializer_class = PostScreenSerializer
    def get(self,request,id):
        patient = Patient.objects.get(id = id)
        tests = MedicalAnalysis.objects.filter(patient=patient).order_by('-id')
        serializer = self.serializer_class(tests, many= True)
        return Response({"status":True,"data":serializer.data,"message":"Success"},status=status.HTTP_200_OK)
    
        
# class GetMyActiveScreen(generics.ListAPIView):
#     authentication_classes = [TokenAuthentication,]
#     permission_classes = [IsPatient]
#     serializer_class=PostScreenSerializer
#     def get(self, request):
#         patient= Patient.objects.get(id= request.user.id)
#         newest_prescription = Screen.objects.filter(patient=patient).order_by('-deadline').first()

#         if not newest_prescription:
#             return Response({
#                 "status": False,
#                 "data": None,
#                 "message": "No prescriptions yet"
#             }, status=status.HTTP_200_OK)

#         serializer = self.serializer_class(newest_prescription)
#         return Response({
#             "status": True,
#             "data": serializer.data,
#             "message": "Newest prescription retrieved successfully"
#         }, status=status.HTTP_200_OK)

        


# class PostScreen(generics.CreateAPIView):
#     serializer_class= PostScreenSerializer
#     parser_classes = (parsers.JSONParser)

#     def post(self, request, filename, format=None):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # image= serializer.validated_data['new']
#         # new_screen= TestScreen.objects.create(new = image)
#         serializer.save()
#         return Response({
            
#         # "token": AuthToken.objects.create(user)[1]
#         })
#         # imgstr64 = serializer.validated_data['image']
#         # imgdata = base64.b64decode(imgstr64)
#         # fname = '/tmp/%s.jpg'%(str(screen.id))
#         # with open(fname,'wb') as f:
#         #     f.write(imgdata)
#         # imgname = '%s.jpg'%(str(image.id))
#         # myphoto.image.save(imgname,File(open(fname,'r')))
#         # os.remove(fname)
#         # return Response(new_screen.data,status= status.HTTP_400_BAD_REQUEST)
        
        
        
        
# class UserUploadedPicture(APIView):
    
#     # parser_classes = (parsers.MultiPartParser, parsers.FormParser)
#     serializer_class =PostScreenSerializer
#     def post(self,request, format=None):

#         serializer = self.serializer_class(data= request.FILES)
#         # # image= request.data['new']
#         # # file= request.data['file']
#         # # file_path= request.data['file_path']
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # image = request.data['new']
#         # new_screen= TestScreen.objects.create(new = image)
#         # new_screen.save()
#         return Response(status=status.HTTP_200_OK)

    
#     def get(self,request):
#         obj = TestScreen.objects.all()
#         serializer = PostScreenSerializer(obj,many= True)
#         # serializer.is_valid(raise_exception=True)
#         return Response(serializer.data)
    
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
    
# @api_view(['POST'])    
# def UserUploadedPicture(request):
#     if request.method == 'POST' and request.FILES['new']:
#         image = request.FILES['new']
#         new_screen= TestScreen.objects.create(new = image)
#         new_screen.save()
#         return Response(status=status.HTTP_200_OK)
    

# @api_view(['POST'])
# def upload_image(request):
#     try:
#         image = request.data['new']
#     except Exception as e:
#         return JsonResponse(ValidationError(_('not a valid SAMLRequest: {}').format(repr(e))))  

#     # encoded_string = base64.b64encode(image.read()).decode('utf-8')
#     format,imgstr = image.split(';base64,')
    
#     obj= TestScreen.objects.create(text = imgstr)
#     obj.save()

#     return Response( status=status.HTTP_201_CREATED)


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
                            "message":"successful"},
                        status=status.HTTP_200_OK)
        
# class GetOldDoctorPatients(generics.ListAPIView):
#     authentication_classes =[ TokenAuthentication,]
#     permission_classes= [IsDoctor,]
#     serializer_class =GetPrescriptionDoctorPatientClinicalSerializer
#     def get(self,request):
#         doctor = Doctor.objects.get(id = request.user.id)
#         old_patients = Prescription.objects.filter(
#             doctor =doctor,
#             ).exclude(Q(
#                 doctor=doctor)&Q(
#                 patient=F('patient'))&
#                 (Q(cancelation_date__isnull=True)|Q(cancelation_date__isnull=False))
#                 ).distinct()
#         if not old_patients :
#             return Response({"status":False,"data":None,'message':'Old patients do not exist'})
#         unique_patients = []
#         unique_ids = set()
#         for patient in old_patients:
#             if patient.patient.id not in unique_ids:
#                 unique_patients.append(patient)
#                 unique_ids.add(patient.patient.id)   
#         serializer =self.serializer_class(unique_patients,many = True)
#         return Response({"status":True,
#                             "data":serializer.data,
#                             "message":"successful"},
#                         status=status.HTTP_200_OK)
        
class GetAllDoctorPatients(generics.ListAPIView):
    authentication_classes =[ TokenAuthentication,]
    permission_classes= [IsDoctor,]
    serializer_class =GetPrescriptionDoctorPatientClinicalSerializer
    def get(self,request):
        doctor = Doctor.objects.get(id = request.user.id)
        All_patients= Prescription.objects.filter(doctor = doctor.id).order_by('-id')
        if not All_patients :
            return Response({"status":False,"data":None,'message':'No Patients to display.'})
        unique_patients = []
        unique_ids = set()
        for patient in All_patients:
            if patient.patient.id not in unique_ids:
                unique_patients.append(patient)
                unique_ids.add(patient.patient.id)           
        serializer =self.serializer_class(unique_patients,many = True)
        return Response({"status":True,
                            "data":serializer.data,
                            "message":"successful"},
                        status=status.HTTP_200_OK)

class GetAllBookedPatients(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsDoctor]
    serializer_class = GetTodayPatientSerializer

    def list(self, request):
        doctor = Doctor.objects.get(id=request.user.id)
        bookings = Booking.objects.filter(doctor=doctor)
        patient_booked_today = PatientBooking.objects.filter(
            booking__in=bookings,
            booking__date__gte=date.today(),
        ).order_by('booking__id')

        if not patient_booked_today.exists():
            return Response({
                "status": True,
                "count": patient_booked_today.count(),
                "data": None,
                "message": "No patients yet."
            }, status=status.HTTP_200_OK)

        serializer = self.serializer_class(patient_booked_today, many=True)
        return Response({
            "status": True,
            "count": patient_booked_today.count(),
            "data": serializer.data,
            "message": "successful"
        }, status=status.HTTP_200_OK)

class GetBookedPatientsInSpecificClinic(generics.ListAPIView):
    authentication_classes =[ TokenAuthentication,]
    permission_classes= [IsDoctor,]
    serializer_class=GetTodayPatientSerializer
    def get(self, request, id):
        doctor = Doctor.objects.get(id =request.user.id)
        try:
            Clinical.objects.get(id=id, doctor=doctor)
        except Clinical.DoesNotExist:
            return Response({
                "status": False,
                "data": None,
                "message": "Clinic not found."
            }, status=status.HTTP_404_NOT_FOUND)
        bookings= Booking.objects.filter(doctor= doctor, clinical =id)
        if not bookings:
            return Response({"status":False,
                        "data":None,
                        "message":"No Appointments yet, add one at least."},
                        status=status.HTTP_404_NOT_FOUND)
        patient_booked = PatientBooking.objects.filter(booking__in=bookings)
        if not patient_booked:
            return Response({"status":False,
                        "data":None,
                        "message":"No patients yet."},
                        status=status.HTTP_404_NOT_FOUND)
        today = date.today()
        # patient_booked_to_delete = patient_booked.filter(booking__date__lt=today)
        # if patient_booked_to_delete:
        #     patient_booked_to_delete.delete()  
        patient_booked_today = patient_booked.filter(booking__date__gte=today).order_by('id')
        if not patient_booked_today:
            return Response({"status":False,
                        "data":None,
                        "message":"No patients yet."},
                        status=status.HTTP_404_NOT_FOUND)
        serializer= self.serializer_class(patient_booked_today, many=True)
        return Response({"status":True,
                        "count":patient_booked_today.count(),
                        "data":serializer.data,
                        "message":"successful"},
                        status=status.HTTP_200_OK)



class GetBookedPatientsInSpecificBooking(generics.ListAPIView):
    authentication_classes =[ TokenAuthentication,]
    permission_classes= [IsDoctor,]
    serializer_class=GetTodayPatientSerializer
    def get(self, request, id):
        doctor = Doctor.objects.get(id =request.user.id)
        try:
            appointmant=Booking.objects.get(id=id, doctor=doctor)
        except Booking.DoesNotExist:
            return Response({
                "status": False,
                "data": None,
                "message": "Appointment not found."
            }, status=status.HTTP_404_NOT_FOUND)
        patient_booked = PatientBooking.objects.filter(booking=appointmant)
        if not patient_booked:
            return Response({"status":False,
                        "data":None,
                        "message":"No patients yet."},
                        status=status.HTTP_404_NOT_FOUND)
        today = date.today()
        # patient_booked_to_delete = patient_booked.filter(booking__date__lt=today)
        # if patient_booked_to_delete:
        #     patient_booked_to_delete.delete()  
        patient_booked_today = patient_booked.filter(booking__date__gte=today)
        if not patient_booked_today:
            return Response({"status":False,
                        "data":None,
                        "message":"No patients yet."},
                        status=status.HTTP_404_NOT_FOUND)
        serializer= self.serializer_class(patient_booked_today, many=True)
        return Response({"status":True,
                        "count":patient_booked_today.count(),
                        "data":serializer.data,
                        "message":"successful"},
                        status=status.HTTP_200_OK)








        
        
class GetTodayBookedPatientsInClinic(generics.ListAPIView):
    authentication_classes =[ TokenAuthentication,]
    permission_classes= [IsDoctor,]
    serializer_class=GetTodayPatientSerializer
    def get(self, request):
        doctor = Doctor.objects.get(id =request.user.id)
        today = date.today()
        bookings= Booking.objects.filter(doctor= doctor, date=today)
        if not bookings:
            return Response({"status":False,
                        "booking_count":0,
                        "data":None,
                        "message":"No Appointments match today yet."},
                        status=status.HTTP_200_OK)
        patient_booked = PatientBooking.objects.filter(booking__in=bookings).order_by('booking__id','id')
        today_patient_consultaion = Prescription.objects.filter(doctor=doctor ,next_consultation=today, cancelation_date__isnull=True)
        if not patient_booked and not today_patient_consultaion:
            return Response({"status":False,
                        "booking_count":patient_booked.count(),
                        "data":None,
                        "message":"No patients yet."},
                        status=status.HTTP_200_OK)
        serializer= self.serializer_class(patient_booked, many=True)
        serializer2=GetPrescriptionDoctorPatientClinicalSerializer(today_patient_consultaion, many = True)
        return Response({"status":True,
                         "total_count":patient_booked.count()+today_patient_consultaion.count(),
                        "booking_count":patient_booked.count(),
                        "consultaion_count":today_patient_consultaion.count(),
                        "booking":serializer.data,
                        "consultaion":serializer2.data,
                        "message":"successful"},
                        status=status.HTTP_200_OK)

class GetTodayBookedPatientsInClinicFirst10(generics.ListAPIView):
    authentication_classes =[ TokenAuthentication,]
    permission_classes= [IsDoctor,]
    serializer_class=GetTodayPatientSerializer
    def get(self, request):
        doctor = Doctor.objects.get(id =request.user.id)
        today = date.today()
        bookings= Booking.objects.filter(doctor= doctor, date=today)
        if not bookings:
            return Response({"status":False,
                        "booking_count":0,
                        "consultaion_count":0,
                        "data":None,
                        "message":"No Appointments match today yet."},
                        status=status.HTTP_200_OK)
        patient_booked = PatientBooking.objects.filter(booking__in=bookings).order_by('booking__id','id')[:5]
        today_patient_consultaion = Prescription.objects.filter(doctor=doctor ,next_consultation=today, cancelation_date__isnull=True)[:5]
        if not patient_booked and not today_patient_consultaion:
            return Response({"status":False,
                        "booking_count":patient_booked.count(),
                        "consultaion_count":today_patient_consultaion.count(),
                        "data":None,
                        "message":"No patients yet."},
                        status=status.HTTP_200_OK)
        serializer= self.serializer_class(patient_booked, many=True)
        serializer2=GetPrescriptionDoctorPatientClinicalSerializer(today_patient_consultaion, many = True)
        return Response({"status":True,
                         "total_count":patient_booked.count()+today_patient_consultaion.count(),
                        "booking_count":patient_booked.count(),
                        "consultaion_count":today_patient_consultaion.count(),
                        "booking":serializer.data,
                        "consultaion":serializer2.data,
                        "message":"successful"},
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
            return Response({"status":False,"data":None,"message":"No new prescription yet."},status=status.HTTP_200_OK)
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
                    
        return Response({"status":True,"data":serializer,"message":"Success"},status=status.HTTP_200_OK)

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
        old_prescriptions = Prescription.objects.filter(patient = patient, cancelation_date__isnull=False ).order_by('-id')
        if not old_prescriptions:
            return Response({"status":False,"data":None,"message":"No prescriptions yet."},status=status.HTTP_200_OK)
        serializer=[]
        for p in old_prescriptions:
            doctor = Doctor.objects.get(id = p.doctor.id)
            clinical = Clinical.objects.get (id =p.clinical.id)
            prescription_serializer = GetPrescriptionSerializer(p).data
            doctor_serializer = ListPrescriptionsDoctor(doctor).data
            clinical_serializer = ListPrescriptionsClinical(clinical).data
            ser = [{"prescription":prescription_serializer,"doctor":doctor_serializer,"clinical":clinical_serializer}]
            serializer = serializer + ser
        return Response({"status":True,"data":serializer,"message":"Success"},status=status.HTTP_200_OK)
    
    
class GetSpecificOldPrescription(generics.ListAPIView):
    permission_classes = [IsPatient,]
    authentication_classes = [TokenAuthentication,]
    def get(self, request,p_id):
        patient= Patient.objects.get(id= request.user.id)
        try:
            old_prescriptions = Prescription.objects.get(id = p_id,patient= patient)
        except Prescription.DoesNotExist:
            return Response({"status":False,"data":None,"message":"No prescriptions with this ID."},status=status.HTTP_200_OK)
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
                    
        return Response({"status":True,"data":serializer,"message":"Success"},status=status.HTTP_200_OK)
    
    

class SetAppointmentForDoctors(generics.CreateAPIView):
    permission_classes = [IsDoctor,]
    authentication_classes = [TokenAuthentication,]
    serializer_class= PostBookingSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor = Doctor.objects.get (id = request.user.id)
        doctor_clinicals= Clinical.objects.filter(doctor=doctor)
        id_list = []
        for obj in doctor_clinicals:
            id_list.append(obj.id)
        if serializer.validated_data['clinical'].id not in id_list:
            return Response({"status":False,
                                "data":None,
                                "message":"Clinic Not found"}
                                ,status=status.HTTP_404_NOT_FOUND)
        clinical=Clinical.objects.get(id=serializer.validated_data['clinical'].id)
        serializer.save(doctor,clinical)
        return Response({"status":True,
                             "data":serializer.data,
                             "message":"Success"}
                            ,status=status.HTTP_201_CREATED)       
class ModifySpecificAppointmentForDoctor(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsDoctor,]
    authentication_classes = [TokenAuthentication,]
    serializer_class= PostBookingSerializer
    def get(self, request,id):
        doctor =Doctor.objects.get(id= request.user.id)
        my_appointments = Booking.objects.filter(doctor =doctor)
        id_list = []
        for obj in my_appointments:
            id_list.append(obj.id)
        if id not in id_list:
            return Response({"status":True,
                             "data":None,
                             "message":"Appointment not dound"}
                            ,status=status.HTTP_404_NOT_FOUND)  
        appointment =Booking.objects.get(id=id)
        serializer = BookingSerializer(appointment)
        return Response({"status":True,
                             "data":serializer.data,
                             "message":"Success"}
                            ,status=status.HTTP_200_OK)      
    def put(self, request,id):
        serializer =self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor =Doctor.objects.get(id= request.user.id)
        my_appointments = Booking.objects.filter(doctor =doctor)
        id_list = []
        for obj in my_appointments:
            id_list.append(obj.id)
        if id not in id_list:
            return Response({"status":True,
                             "data":None,
                             "message":"Appointment not dound"}
                            ,status=status.HTTP_404_NOT_FOUND)  
        today = timezone.now().date()
        weekday = serializer.validated_data['available_day_of_week']
        days_until_available_day = (weekday - today.weekday()) % 7
        available_date = today + datetime.timedelta(days=days_until_available_day)
        appointment =Booking.objects.get(id=id)
        clinical = serializer.validated_data['clinical']
        # date = serializer.validated_data['date']
        start = serializer.validated_data['start']
        end = serializer.validated_data['end']
        allowed_number = serializer.validated_data['allowed_number']
        appointment.clinical=clinical
        appointment.date=available_date
        appointment.start=start
        appointment.start=start
        appointment.end=end
        appointment.allowed_number=allowed_number
        appointment.save()
        # serializer.save()
        return Response({"status":True,
                             "data":None,
                             "message":"Success"}
                            ,status=status.HTTP_200_OK)      
    def delete(self, request,id):
        doctor =Doctor.objects.get(id= request.user.id)
        my_appointments = Booking.objects.filter(doctor =doctor)
        id_list = []
        for obj in my_appointments:
            id_list.append(obj.id)
        if id not in id_list:
            return Response({"status":True,
                             "data":None,
                             "message":"Appointment not dound"}
                            ,status=status.HTTP_404_NOT_FOUND)  
        appointment =Booking.objects.get(id=id)
        appointment.delete()
        return Response({"status":True,
                             "data":None,
                             "message":"Success"}
                            ,status=status.HTTP_200_OK)      
class GetMyAllAppointmentsForDoctor(generics.ListAPIView):
    permission_classes = [IsDoctor,]
    authentication_classes = [TokenAuthentication,]
    serializer_class= BookingSerializer
    def get(self, request):
        doctor = Doctor.objects.get(id = request.user.id)
        my_all_appointments = Booking.objects.filter(doctor=doctor)
        if not my_all_appointments:
            return Response({"status":False,
                        "data":None,
                        "message":"No Appointments Yet."},
                    status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(my_all_appointments,many = True)
        return Response({"status":True,
                        "data":serializer.data,
                        "message":"success"},
                    status=status.HTTP_200_OK)
        
class GetMyAllAppointmentsForPatient(generics.ListAPIView):
    permission_classes = [IsPatient,]
    authentication_classes = [TokenAuthentication,]
    serializer_class= BookingSerializer
    def get(self, request,d_id,id):
        doctor = Doctor.objects.get(id = d_id)
        try:
            appointment = Booking.objects.get(doctor=doctor,id =id)
        except Booking.DoesNotExist:
            return Response({"status":False,
                        "data":None,
                        "message":" Error 404.<br> No Appointment with this id."},
                    status=status.HTTP_404_NOT_FOUND)
        patient_number = PatientBooking.objects.filter(booking__id=id).count() +1
        serializer = self.serializer_class(appointment,many = False)
        doctor_serializer = GetDoctorSerializer(doctor, many= False)
        return Response({"status":True,
                        "data": serializer.data,
                        "doctor_data":doctor_serializer.data,
                        "patient_number":patient_number,
                        "message":"success"},
                    status=status.HTTP_200_OK)
        
class GetAllAppointmentsForDoctor(generics.ListAPIView):
    permission_classes = [IsPatient,]
    authentication_classes = [TokenAuthentication,]
    serializer_class= BookingSerializer
    def get(self, request,id):
        # doctor = Doctor.objects.get(id =id)
        my_all_appointments = Booking.objects.filter(
            Q(patientbooking__isnull=True) |
            Q(allowed_number__gt=Subquery(
                PatientBooking.objects.filter(
                    booking_id=OuterRef('id')
                ).values('booking_id').annotate(
                    count=Count('booking_id')
                ).values('count')
            )),
            doctor=id,
        )
        if not my_all_appointments:
            return Response({"status":False,
                        "data":None,
                        "message":"No Appointments Yet."},
                    status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(my_all_appointments,many = True)
        return Response({"status":True,
                        "data":serializer.data,
                        "message":"success"},
                    status=status.HTTP_200_OK)
        
class ListClinical(generics.ListCreateAPIView):
    permission_classes = [IsDoctor,]    
    authentication_classes = [TokenAuthentication,]
    serializer_class= ListClinicalSerializer
    def get(self, request):
        doctor = Doctor.objects.get(id = request.user.id)
        my_all_clinics = Clinical.objects.filter(doctor=doctor).order_by('-id')
        if not my_all_clinics:
            return Response({"status":False,
                            "data":None,
                            "message":"No clinics Yet"},
                        status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(my_all_clinics,many = True)
        return Response({"status":True,
                            "data":serializer.data,
                            "message":"successful"},
                        status=status.HTTP_200_OK)    
    def create(self, request):
        doctor = Doctor.objects.get(id = request.user.id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_clinic=Clinical.objects.create(
            clinical_name=serializer.validated_data['clinical_name'],
            clinical_location=serializer.validated_data['clinical_location'],
            telephone=serializer.validated_data['telephone'],
            phone=serializer.validated_data['phone'],
            doctor=doctor
        )
        data=self.serializer_class(new_clinic,many=False)
        return Response({"status":True,
                    "data":data.data,
                    "message":"successful"},
                status=status.HTTP_200_OK)  
        
        
        
class GetSpecificClinical(generics.ListAPIView):
    permission_classes = [IsDoctor,]
    authentication_classes = [TokenAuthentication,]
    serializer_class= UpdateSpecificClinicalSerializer
    
    def get(self, request,id):
        doctor = Doctor.objects.get(id = request.user.id)
        try:
            specific_clinical=Clinical.objects.get(id=id)
            if specific_clinical.doctor.id != doctor.id:
                return Response({"status":False,
                                "data":None,
                                "message":"You have not clinic with this ID"},
                            status=status.HTTP_404_NOT_FOUND)
        except Clinical.DoesNotExist:
            return Response({"status":False,
                                "data":None,
                                "message":"You have not clinic with this ID"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(specific_clinical,many = False)
        return Response({"status":True,
                            "data":serializer.data,
                            "message":"successful"},
                        status=status.HTTP_200_OK) 
    def put(self,request,id):
        doctor = Doctor.objects.get(id = request.user.id)
        try:
            specific_clinical=Clinical.objects.get(id=id)
            if specific_clinical.doctor.id != doctor.id:
                return Response({"status":False,
                                "data":None,
                                "message":"You have not clinic with this ID"},
                            status=status.HTTP_404_NOT_FOUND)
        except Clinical.DoesNotExist:
            return Response({"status":False,
                                "data":None,
                                "message":"You have not clinic with this ID"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(specific_clinical,data=request.data,partial= True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":True,
                            "data":None,
                            "message":"successful"},
                        status=status.HTTP_200_OK)   
    
    def delete(self,request,id):
        doctor = Doctor.objects.get(id = request.user.id)
        try:
            specific_clinical=Clinical.objects.get(id=id)
            if specific_clinical.doctor.id != doctor.id:
                return Response({"status":False,
                                "data":None,
                                "message":"You have not clinic with this ID"},
                            status=status.HTTP_404_NOT_FOUND)
        except Clinical.DoesNotExist:
            return Response({"status":False,
                                "data":None,
                                "message":"You have not clinic with this ID"},
                            status=status.HTTP_404_NOT_FOUND)
        specific_clinical.delete()
        return Response({"status":True,
                            "data":None,
                            "message":"successful"},
                        status=status.HTTP_200_OK)  
        
class BookingApi(generics.ListAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsPatient,]
    def get(self,request , id):
        appointment = Booking.objects.get(id = id)
        patients_have_booked = PatientBooking.objects.filter(booking__id=id).count() 
        if (appointment.allowed_number == patients_have_booked):
            return Response ({"status":False,
                              "data":None,
                              "message":"The appointment is completed."},status=status.HTTP_400_BAD_REQUEST)
        elif (appointment.allowed_number > patients_have_booked):
            patient = Patient.objects.get(id= request.user.id)
            try:
                PatientBooking.objects.get(patient = patient)
                return Response ({"status":False,
                              "data":None,
                              "message":"You already booked an appointment."},status=status.HTTP_400_BAD_REQUEST)
            except PatientBooking.DoesNotExist:                
                PatientBooking.objects.create(
                    patient= patient,
                    booking = appointment
                )
                return Response ({"status":True,
                              "data":None,
                              "message":"Success."},status=status.HTTP_200_OK)
        return Response ({"status":False,
                              "data":None,
                              "message":"Error."},status=status.HTTP_400_BAD_REQUEST)
        
        
class GetInterAction(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsDoctor,]
    def post(self, request):
        if request.data:
            base = request.data['base']
            new= request.data['new']
            try:
                new_drug=StandardDrugs.objects.get(name=new)
                base_drugs= StandardDrugs.objects.filter(name=base).all()
                base_drugs=base_drugs.values_list('activeIngredient', flat=True)
                interaction =ingredient_interaction.objects.filter(first=new_drug.activeIngredient,
                            second__in=base_drugs
                            ) or ingredient_interaction.objects.filter(
                            first__in=base_drugs,
                            second=new_drug.activeIngredient)
                if interaction:
                    serializer =ser.serialize('json', interaction)
                    return Response({"status":True,"data":serializer,"message":"Success"},status=status.HTTP_200_OK)
                else:
                    return Response({"status":False,"data":None,"message":"No interactions"},status=status.HTTP_404_NOT_FOUND)
                    
            except StandardDrugs.DoesNotExist:
                return Response({"status":False,"data":None,"message":"No Drugs with this name"},status=status.HTTP_404_NOT_FOUND)
        else:
                return Response({"status":False,"data":None,"message":"Please Enter new and base"},status=status.HTTP_400_BAD_REQUEST)
            

class MyPatientDisease(generics.ListCreateAPIView):
    authentication_classes= [TokenAuthentication,]
    permission_classes= [IsPatient,]
    serializer_class=GetPatientDiseaseSerializer
    
    def get(self, request):
        patient = Patient.objects.get(id = request.user.id)
        disease = PatientDiseases.objects.filter(patinet=patient)
        if not disease:
            return Response({"status":False,
                         "data":None,
                         "message":"No disease"}
                        ,status=status.HTTP_200_OK)
        serializer = self.serializer_class(disease, many = True)
        return Response({"status":True,
                         "data":serializer.data,
                         "message":"Success"}
                        ,status=status.HTTP_200_OK)
    def post(self, request):
        serializer=PatientDiseasesSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        patient = Patient.objects.get(id = request.user.id)
        try:
            PatientDiseases.objects.get(patinet=patient, disease=serializer.validated_data['disease'])
            return Response({"status":False,
                         "data":None,
                         "message":"This disease already exist."}
                        ,status=status.HTTP_400_BAD_REQUEST)
            
        except PatientDiseases.DoesNotExist :
            PatientDiseases.objects.create(
                patinet=patient,
                disease=serializer.validated_data['disease'],
                disease_date=serializer.validated_data['disease_date'],
            )
            return Response({"status":True,
                         "data":None,
                         "message":"Success"}
                        ,status=status.HTTP_201_CREATED)
            
            
class ChronicDiseaseView(generics.ListAPIView):
    authentication_classes= [TokenAuthentication,]
    permission_classes= [IsPatient,]
    serializer_class=ChronicDiseaseSerializer
    
    def get(self, request):
        chronic_disease= ChronicDiseases.objects.all()
        serializer =self.serializer_class(chronic_disease, many=True)
        return Response({"status":True,"data":serializer.data,"message":"Sucssess"},status=status.HTTP_200_OK)
    
class StandardScreensView(generics.ListAPIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes= [IsDoctor,]
    serializer_class=StandardScreensSerializer
    def get(self, request):
        standard_screens =StandardScreens.objects.all()
        serializer= self.serializer_class(standard_screens, many=True)
        return Response({"status":True,"data":serializer.data,"message":"Success"},status=status.HTTP_200_OK)


class StandardTestView(generics.ListAPIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes= [IsDoctor,]
    serializer_class=StandardMedicalAnalysisSerializer
    def get(self, request):
        standard_tests =StandardMedicalAnalysis.objects.all()
        serializer= self.serializer_class(standard_tests, many=True)
        return Response({"status":True,"data":serializer.data,"message":"Success"},status=status.HTTP_200_OK)
    
class CommitmentView(generics.ListCreateAPIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes= [IsPatient,]
    # serializer_class =SetDrugSerializer
    def post(self, request, id):
        obj = PatientCommitment.objects.get(id=id, patient=request.user.id)
        allowed_time = obj.date + timedelta(days=1)
        current_time = timezone.now()

        if current_time > allowed_time:
            return Response({"status": False, "data": None, "message": "Failed"}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data['status']
        if data == True:
            obj.status = data
            obj.save()
            prescription = Prescription.objects.get(drug__patientcommitment__id=id)
            drugs= Drug.objects.filter(prescription=prescription)
            if drugs.count() >0:
                _sum=0
                for drug in drugs:
                    _sum = _sum+drug.commitmentRatio()
                prescription.Commitment_ratio=_sum / drugs.count()
                prescription.save()
            return Response({"satus":True,"data":None,"message":"Success"},status=status.HTTP_200_OK)
        elif data == False:
            obj.status = data
            obj.save()
            prescription = Prescription.objects.get(drug__patientcommitment__id=id)
            drugs= Drug.objects.filter(prescription=prescription)
            if drugs.count() >0:
                _sum=0
                for drug in drugs:
                    _sum = _sum+drug.commitmentRatio()
                prescription.Commitment_ratio=_sum / drugs.count()
                prescription.save()
            return Response({"satus":False,"data":None,"message":"Success"},status=status.HTTP_200_OK)
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
