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
        fields = ['case', 'plane', 'position', 'img']
        
        
class CaseSerializer(serializers.ModelSerializer):
    slice_img = ImageSerializer(many=True)
    class Meta:
        model = Case
        fields = ['patient', 'slug', 'order', 'title', 'created', 'number_nods', 
                  'annotations', 'predictions', 'ct', 'slice_img']
        
        
class PatientSerializer(serializers.ModelSerializer):
    cases = CaseSerializer(many=True)
    #pdb.set_trace()
    
    class Meta:
        model = Patient
        fields = ['subject', 'owner', 'id', 'name', 'surname', 'slug', 'age',
                  'created', 'gender', 'race', 'height', 'weight', 'alive', 'smoker',
                  'comments', 'med_history', 'evolution_treatment', 'cases']