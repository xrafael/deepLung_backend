from rest_framework import serializers
from ..models import Subject, Patient, Case, ModelImages
import pdb


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']
        

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelImages
        fields = ['plane', 'position', 'img']
        
        
class CaseSerializer(serializers.ModelSerializer):
    slice_img = ImageSerializer(many=True)
    class Meta:
        model = Case
        fields = ['order', 'title', 'created', 'ct', 'slice_img']
        
        
class PatientSerializer(serializers.ModelSerializer):
    cases = CaseSerializer(many=True)
    #pdb.set_trace()
    
    class Meta:
        model = Patient
        fields = ['id', 'name', 'surname', 'slug', 'age',
                  'created', 'gender', 'race', 'cases']