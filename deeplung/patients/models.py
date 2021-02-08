from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
import uuid


GENDER_CHOICES = (
    (0, 'male'),
    (1, 'female'),
    (2, 'not specified'),
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
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=60)
    age = models.PositiveSmallIntegerField()
    gender = models.IntegerField(choices=GENDER_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.surname


class Case(models.Model):
    patient = models.ForeignKey(Patient,
                               related_name='cases',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    anamnesis = models.TextField()
    order = OrderField(blank=True, for_fields=['patient'])

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']


class Study(models.Model):
    case = models.ForeignKey(Case,
                               related_name='studys',
                               on_delete=models.CASCADE)
    study_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':(
                                     'text',
                                     'video',
                                     'image',
                                     'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('study_type', 'object_id')
    order = OrderField(blank=True, for_fields=['case'])

    class Meta:
        ordering = ['order']



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

class Text(ItemBase):
    study = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
       file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()
