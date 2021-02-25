from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField, ShortUUIDField
from django.template.loader import render_to_string
from multiupload.fields import MultiImageField
from deeplung.settings import MEDIA_ROOT

import matplotlib.pyplot as plt
from pydicom import dcmread
import numpy as np
import nibabel as nib
import PIL.Image
from PIL.Image import fromarray
import os
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
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True)
    race = models.IntegerField(choices=RACE_CHOICES, blank=True, null=True)
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
    number_nods = models.PositiveSmallIntegerField(blank=True, null=True)
    predictions = models.TextField(max_length=180, blank=True)
    annotations = models.TextField(max_length=180, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    order = OrderField(blank=True, for_fields=['patient'])
    ct = models.FileField(upload_to='files/')
    slices = models.TextField(blank=True, null=True, editable=False)
    
    def get_slices(obj):
        #pdb.set_trace()
        if hasattr(obj, 'ct'):
            
            idxs = [i+1 for i in range(len(obj.ct.path)) if obj.ct.path[i]=='/']
            name = MEDIA_ROOT + 'tmp/' + obj.ct.path[idxs[-1]:]
            with open(name, 'wb') as f:
                f.write(obj.ct.read())
                
            img = nib.load(name)
            #pdb.set_trace()
            #print(img.get_fdata().shape)
            images = [np.array(img.get_fdata()[:,:,i]) 
                      for i in range(img.get_fdata().shape[2])]
            images8 = [((images[j]-np.min(images[j]))/(np.max(images[j])-
                       np.min(images[j]))*255).astype(np.uint8) 
                       for j in range(len(images))]
            #pdb.set_trace()
            os.remove(name)
            return images8
    
    def save(self, *args, **kwargs):
        if hasattr(self.ct, 'path'):
            imgs = self.get_slices()
            str_txt = ''
            if not os.path.exists(MEDIA_ROOT +'images/' + self.patient.slug + '/'):
                os.makedirs(MEDIA_ROOT + 'images/' + self.patient.slug + '/')
            #pdb.set_trace()
            for i, img in enumerate(imgs):
                name = (MEDIA_ROOT + 'images/' + self.patient.slug + '/' +
                        self.slug + '_ax_' + str(i).zfill(3) + '.png')
                fromarray(img, 'L').save(name)
                #pdb.set_trace()
                str_txt += 'ax\t' + str(i).zfill(3) + '\t' + name + '\n'
            
            with open(MEDIA_ROOT + 'img_data/' + self.patient.slug + '_' +
                      self.slug + '.txt', 'w') as f:
                f.write(str_txt)
            
            #pdb.set_trace()
            self.slices = (MEDIA_ROOT + 'img_data/' + self.patient.slug + '_' +
                           self.slug + '.txt')
            
        super(Case, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']
        
        
#class ModelImages(models.Model):
#    case = models.ForeignKey(Case, on_delete=models.CASCADE,
#                              related_name="slices_images")
#    img = models.ImageField(blank=True, null=True)
#    
#    def save(name, content, *args, **kwargs):
#        pdb.set_trace()
#        ModelImages(self).img = self.mainimage
#        #ModelImages().img.save()
#        super().save(*args, **kwargs)
#    
#    class Meta:
#        abstract = True
#
#    def __str__(self):
#        return self.image
#    
#    def render(self):
#        return render_to_string(f'patients/content/file.html',
#                                {'item': self})
    #self.save()


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
