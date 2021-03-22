from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField, ShortUUIDField
from django.template.loader import render_to_string
from multiupload.fields import MultiImageField
from deeplung.settings import MEDIA_ROOT
from django.db.models.signals import post_save
from django.db import transaction

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
import asyncio


#def rand_slug(n):
#    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))
#
#def UniqueID(max_length, for_fields):
#    value = models.CharField(max_length=max_length, unique=True, 
#                             default=rand_slug(), editable=False)
#    #pdb.set_trace()
#    return value
    
PLANE_CHOICES = (
    (0, 'axial'),
    (1, 'sagittal'),
    (2, 'coronal'),
)    
    
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
    alive = models.BooleanField(blank=True, null=True)
    smoker = models.BooleanField(blank=True, null=True)
    comments = models.TextField(max_length=180, blank=True)
    med_history = models.TextField(max_length=180, blank=True)
    evolution_treatment = models.TextField(max_length=180, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.slug}. {self.name}. {self.surname}'


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
    #slices = models.FileField(upload_to='img_data/', blank=True, null=True, editable=False)
    
    #def get_slices(obj):
    #    #pdb.set_trace()
    #    if hasattr(obj, 'ct'):
    #        
    #        idxs = [i+1 for i in range(len(obj.ct.path)) if obj.ct.path[i]=='/']
    #        name = MEDIA_ROOT + 'tmp/' + obj.ct.path[idxs[-1]:]
    #        with open(name, 'wb') as f:
    #            f.write(obj.ct.read())
    #            
    #        img = nib.load(name)
    #        #pdb.set_trace()
    #        #print(img.get_fdata().shape)
    #        images = [np.array(img.get_fdata()[:,:,i]) 
    #                  for i in range(img.get_fdata().shape[2])]
    #        images8 = [((images[j]-np.min(images[j]))/(np.max(images[j])-
    #                   np.min(images[j]))*255).astype(np.uint8) 
    #                   for j in range(len(images))]
    #        #pdb.set_trace()
    #        os.remove(name)
    #        return images8
    
    #def save(self, *args, **kwargs):
    #    super(Case, self).save(*args, **kwargs)
    #    if hasattr(self.ct, 'path'):
    #        imgs = self.get_slices()
    #        str_txt = ''
    #        if not os.path.exists(MEDIA_ROOT +'images/' + self.patient.slug + '/'):
    #            os.makedirs(MEDIA_ROOT + 'images/' + self.patient.slug + '/')
    #        #pdb.set_trace()
    #        for i, img in enumerate(imgs):
    #            name = (MEDIA_ROOT + 'images/' + self.patient.slug + '/' +
    #                    self.slug + '_ax_' + str(i).zfill(3) + '.png')
    #            fromarray(img, 'L').save(name)
    #            #pdb.set_trace()
    #            str_txt += 'ax\t' + str(i).zfill(3) + '\t' + name + '\n'
    #        
    #        with open(MEDIA_ROOT + 'img_data/' + self.patient.slug + '_' +
    #                  self.slug + '.txt', 'w') as f:
    #            f.write(str_txt)
    #        
    #        #pdb.set_trace()
    #        self.slices = ('img_data/' + self.patient.slug + '_' +
    #                       self.slug + '.txt')
    #        #self.slices.save()
    #        super(Case, self).save(*args, **kwargs)
            
        
#    def save(self, *args, **kwargs):
#        if hasattr(self.ct, 'path'):
#            imgs = self.get_slices()
#            str_txt = ''
#            if not os.path.exists(MEDIA_ROOT +'images/' + self.patient.slug + '/'):
#                os.makedirs(MEDIA_ROOT + 'images/' + self.patient.slug + '/')
#            pdb.set_trace()
#            for i, img in enumerate(imgs):
#                name = self.slug + '_ax_' + str(i).zfill(3) + '.png'
#                name = (MEDIA_ROOT + 'images/' + self.patient.slug + '/' +
#                        self.slug + '_ax_' + str(i).zfill(3) + '.png')
#                fromarray(img, 'L').save(name)
#                #pdb.set_trace()
#                str_txt += 'ax\t' + str(i).zfill(3) + '\t' + name + '\n'
#            
#            with open(MEDIA_ROOT + 'img_data/' + self.patient.slug + '_' +
#                      self.slug + '.txt', 'w') as f:
#                f.write(str_txt)
#            
#            #pdb.set_trace()
#            self.slices = (MEDIA_ROOT + 'img_data/' + self.patient.slug + '_' +
#                           self.slug + '.txt')
#            
#        super(Case, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.patient}. {self.slug}. {self.title}'

    class Meta:
        ordering = ['order']
        
        
class ModelImages(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE,
                              related_name="slice_img")
    img = models.ImageField(editable=False)
    plane = models.IntegerField(choices=PLANE_CHOICES, editable=False)
    position = models.PositiveSmallIntegerField(editable=False)
    
    #def save(name, content, *args, **kwargs):
    #    pdb.set_trace()
    #    ModelImages(self).img = self.mainimage
    #    #ModelImages().img.save()
    #    super().save(*args, **kwargs)
    
    #def save(self, *args, **kwargs):
    #    pdb.set_trace()
    #    if self.img:
    #        pdb.set_trace()
    #    super(ModelImages, self).save(*args, **kwargs)
    def __str__(self):
        return f'{self.case}. {self.plane}. {self.position}'
    
    class Meta:
        ordering = ['position']
    #    abstract = True
    
    #def render(self):
    #    return render_to_string(f'patients/content/file.html',
    #                            {'item': self})
    #self.save()

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
    

def process_3d_image(sender, instance, created, **kwargs):
    # this is run only on first save (creation)
    if created:
        # if get_slices is creating and saving ModelImages objects you can pass
        # the instance (which is the Case object) for the foreign key as well.
        imgs = get_slices(instance)
        if not os.path.exists(MEDIA_ROOT +'images/' + instance.patient.slug + '/'):
            os.makedirs(MEDIA_ROOT + 'images/' + instance.patient.slug + '/')
        for i, img in enumerate(imgs):
            plane = 'ax'
            position = str(i).zfill(3)
            #name = instance.slug + '_ax_' + position + '.png'
            #pdb.set_trace()
            name = (MEDIA_ROOT + 'images/' + instance.patient.slug + '/' +
                    instance.slug + '_' + plane + '_' + position + '.png')
            fromarray(img, 'L').save(name)
            name = name[len(MEDIA_ROOT):]
            #pdb.set_trace()
            case_img = ModelImages(case=instance, img=name, plane=0,
                                   position=position)
            with transaction.atomic():
                #pdb.set_trace()
                case_img.save()
    
    
post_save.connect(process_3d_image, sender=Case)


    
    

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
    
    

