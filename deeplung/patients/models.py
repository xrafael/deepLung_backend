from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField, ShortUUIDField
from django.template.loader import render_to_string
from multiupload.fields import MultiImageField
from pydicom import dcmread
import numpy as np
#import uuid
#import random
#import string 
import pdb


#def rand_slug(n):
#    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))
#
#def UniqueID(max_length, for_fields):
#    value = models.CharField(max_length=max_length, unique=True, 
#                             default=rand_slug(), editable=False)
#    #pdb.set_trace()
#    return value
    
    
    
    
GENDER_CHOICES = (
    (0, 'male'),
    (1, 'female'),
    (2, 'not specified'),
)

RACE_CHOICES = (
    (0, 'caucasian'),
    (1, 'asian'),
    (2, 'african'),
    (3, 'australoid'),
    (4, 'not specified'),
)


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Patient(models.Model):
    owner = models.ForeignKey(User,
                              related_name='patients_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='patients',
                                on_delete=models.CASCADE)
    #unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
    #                            editable=False, unique=True)
    #slug = models.CharField(max_length=6, unique=True, 
    #                        default=rand_slug(6), editable=False)
    slug = ShortUUIDField(max_length=6)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=60)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True)
    race = models.IntegerField(choices=RACE_CHOICES, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    weight = models.PositiveSmallIntegerField(blank=True, null=True)
    alive = models.BooleanField()
    smoker = models.BooleanField()
    comments = models.TextField(max_length=180, blank=True)
    med_history = models.TextField(max_length=180, blank=True)
    evolution_treatment = models.TextField(max_length=180, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.surname


class Case(models.Model):
    patient = models.ForeignKey(Patient,
                               related_name='cases',
                               on_delete=models.CASCADE)
    slug = ShortUUIDField(max_length=3)
    title = models.CharField(max_length=50)
    number_nods = models.PositiveSmallIntegerField()
    predictions = models.TextField(max_length=180, blank=True)
    annotations = models.TextField(max_length=180, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    order = OrderField(blank=True, for_fields=['patient'])
    ct = models.FileField(upload_to='files/')
    images = MultiImageField(min_num=1, max_num=300, max_file_size=None)
    #object_id = models.PositiveIntegerField()
    #files_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #item = GenericForeignKey('files_type', 'object_id')
    
    def get_slices(self):
        dicom = dcmread(self.ct)
        tensor = np.array(dicom.pixel_array)
        pdb.set_trace()
        
        return tensor
        # save single slices
    
    def save(self, *args, **kwargs):
        if not self.images:
            self.images = self.get_slices()
        super(Case, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']


#class Study(models.Model):
#    case = models.ForeignKey(Case,
#                               related_name='studys',
#                               on_delete=models.CASCADE)
#    study_type = models.ForeignKey(ContentType,
#                                     on_delete=models.CASCADE,
#                                     limit_choices_to={'model__in':(
#                                     'text',
#                                     'image',
#                                     'file')})
#    object_id = models.PositiveIntegerField()
#    created = models.DateTimeField(auto_now_add=True)
#    predictions = models.TextField(max_length=180)
#    annotations = models.TextField(max_length=180)
#    item = GenericForeignKey('study_type', 'object_id')
#    order = OrderField(blank=True, for_fields=['case'])
#
#    class Meta:
#        ordering = ['order']



class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
    
    def render(self):
        return render_to_string(f'patients/content/{self._meta.model_name}.html',
                                {'item': self})
    

class Text(ItemBase):
    study = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
       file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()
