from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework.authentication import BasicAuthentication
#from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
#from rest_framework.decorators import action
from ..models import Subject, Patient, Case, ModelImages
from .serializers import SubjectSerializer, PatientSerializer
#from .permissions import IsEnrolled
from deeplung.settings import MEDIA_ROOT
import pdb


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


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
    serializer_class = PatientSerializer

#    @action(detail=True,
#            methods=['post'],
#            authentication_classes=[BasicAuthentication],
#            permission_classes=[IsAuthenticated])
#    def enroll(self, request, *args, **kwargs):
#        course = self.get_object()
#        course.students.add(request.user)
#        return Response({'enrolled': True})
#
#    @action(detail=True,
#            methods=['get'],
#            serializer_class=CourseWithContentsSerializer,
#            authentication_classes=[BasicAuthentication],
#            permission_classes=[IsAuthenticated, IsEnrolled])
#    def contents(self, request, *args, **kwargs):
#        return self.retrieve(request, *args, **kwargs)
#