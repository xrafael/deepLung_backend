from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
#from rest_framework.decorators import action
from ..models import Subject, Patient, Case, ModelImages
from rest_framework.renderers import JSONRenderer
from .serializers import *
#from .permissions import IsEnrolled
from deeplung.settings import MEDIA_ROOT
import os
import pdb


#@api_view(['GET', 'POST'])
#def post_patient(request):
#    """
#    List all code snippets, or create a new snippet.
#    """
#    if request.method == 'GET':
#        patients = Patient.objects.all()
#        serializer = PatientSerializer(patients, many=True)
#        return Response(serializer.data)
#
#    elif request.method == 'POST':
#        pdb.set_trace()
#        patient_data = JSONParser().parse(request)
#        serializer = PatientSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
    
#class HelloApiView(APIView):
#    """Test APIView"""
#
#    #Here we are telling django that the serializer class for this apiViewClass is serializer.HelloSerializer class
#    #serializer_class = serializers.HelloSerializer
#
#    def get(self, request, format=None):
#        """Retruns a list of APIViews features."""
#
#        an_apiview = [
#            'Uses HTTP methods as fucntion (get, post, patch, put, delete)',
#            'It is similar to a traditional Django view',
#            'Gives you the most of the control over your logic',
#            'Is mapped manually to URLs'
#        ]
#    
#        #The response must be as dictionary which will be shown in json as response
#        return Response({'message': 'Hello!', 'an_apiview': an_apiview})
#
#    def post(self,request):
#        """Create a hello message with our name"""
#
#        serializer = PatientSerializer(data=request.data)
#
#        if serializer.is_valid():
#            name = serializer.data.get('name')
#            message = 'Hello! {0}'.format(name)
#            return Response({'message':message})
#        else:
#            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#class CourseEnrollView(APIView):
#    authentication_classes = (BasicAuthentication,)
#    permission_classes = (IsAuthenticated,)
#
#    def post(self, request, pk, format=None):
#        course = get_object_or_404(Course, pk=pk)
#        course.students.add(request.user)
#        return Response({'enrolled': True})
#
#
class PatientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Patient.objects.all()
    #pdb.set_trace()
    # queryset[0].cases.all()[0].slice_img.all()[0]
    
    #for patient in queryset:
    #    for case in patient.cases.all():
    #        #pdb.set_trace()
    #        txt_str = case.slices.read().decode('ascii')
    #        lines = txt_str.split("\n")
    #        for line in lines:
    #            if len(line) > 10:
    #                plane = line[:2]
    #                position = line[3:6]
    #                name = line[7:]
    #                pdb.set_trace()
    #            
    #        
    #        
    #        pdb.set_trace()
    serializer_class = OnlyPatientSerializer
    
class PatientDetailView(generics.RetrieveAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    def get(self, request, *args, **kwargs):
        #pdb.set_trace()
        slug = os.path.basename(os.path.normpath(request.get_full_path()))
        patient = Patient.objects.get(slug=slug)
        
        serializer = PatientSerializer(patient)
        #if serializer.is_valid():
        #    serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PatientCreateView(generics.ListCreateAPIView):
    #pdb.set_trace()
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    #pdb.set_trace()
    #authentication_classes = (BasicAuthentication,)
    #permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        #pdb.set_trace()
        data = request.data
        new_patient = Patient(owner=Patient.objects.all()[0].owner,
                              subject=Subject.objects.all()[0], name=data['name'], 
                              surname=data['surname'], age=data['age'],
                              gender = data['gender'], race = data['race'])
        
        #pdb.set_trace()
        new_patient.save()
        return Response({'posted': True})
    
    
class CaseCreateView(generics.ListCreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    #pdb.set_trace()
    #authentication_classes = (BasicAuthentication,)
    #permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        data = request.data
        #pdb.set_trace()
        new_case = Case(patient=Patient.objects.get(slug=data['patient_slug']),
                        title=data['title'], annotations=data['annotations'],
                        ct=data['ct'])
        
        #pdb.set_trace()
        new_case.save()
        return Response({'posted': True})
    
    

#
#    @action(detail=True,
#            methods=['get'],
#            serializer_class=CourseWithContentsSerializer,
#            authentication_classes=[BasicAuthentication],
#            permission_classes=[IsAuthenticated, IsEnrolled])
#    def contents(self, request, *args, **kwargs):
#        return self.retrieve(request, *args, **kwargs)
#