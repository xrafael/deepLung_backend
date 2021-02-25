from django import forms
from django.forms.models import inlineformset_factory
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField
from .models import Patient, Case
import pdb


CaseFormSet = inlineformset_factory(Patient,
                                      Case,
                                      fields=['title',
                                              'annotations'],
                                      extra=2,
                                      can_delete=True)


#class UploadForm(forms.Form):
#    attachments = MultiFileField(min_num=1, max_num=1024, max_file_size=1024*1024*5)
#
#    # If you need to upload media files, you can use this:
#    attachments = MultiMediaField(
#        min_num=1,
#        max_num=1024,
#        max_file_size=1024*1024*5,
#        media_type='video'  # 'audio', 'video' or 'image'
#    )
#
#    # For images (requires Pillow for validation):
#    attachments = MultiImageField(min_num=1, max_num=1024, max_file_size=1024*1024*5)