from django import forms
from django.forms.models import inlineformset_factory
from .models import Patient, Case


CaseFormSet = inlineformset_factory(Patient,
                                      Case,
                                      fields=['title',
                                              'annotations'],
                                      extra=2,
                                      can_delete=True)
