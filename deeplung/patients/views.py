from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, \
                                      DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, \
                                       PermissionRequiredMixin
from django.forms.models import modelform_factory
from django.apps import apps
from django.views.generic.detail import DetailView
from django.db.models import Count
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from .models import Patient, Case, Subject
from .forms import CaseFormSet
import pdb


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerPatientMixin(OwnerMixin,
                       LoginRequiredMixin,
                       PermissionRequiredMixin):
    model = Patient
    fields = ['slug', 'name', 'surname', 'created']
    success_url = reverse_lazy('manage_patient_list')


class OwnerPatientEditMixin(OwnerPatientMixin, OwnerEditMixin):
    template_name = 'patients/manage/patient/form.html'


class ManagePatientListView(OwnerPatientMixin, ListView):
    template_name = 'patients/manage/patient/list.html'
    permission_required = 'patients.view_patient'

class PatientCreateView(OwnerPatientEditMixin, CreateView):
    permission_required = 'patients.add_patient'
    
#    def post(self, request, *args, **kwargs):
#        pdb.set_trace()
#        if formset.is_valid():
#            formset.save()
#            return redirect('manage_patient_list')
#        return self.render_to_response({'patient': self.patient,
#                                        'formset': formset})


class PatientUpdateView(OwnerPatientEditMixin, UpdateView):
    permission_required = 'patients.change_patient'


class PatientDeleteView(OwnerPatientMixin, DeleteView):
    template_name = 'patients/manage/patient/delete.html'
    permission_required = 'patients.delete_patient'


class PatientCaseUpdateView(TemplateResponseMixin, View):
    template_name = 'patients/manage/case/formset.html'
    patient = None

    def get_formset(self, data=None):
        return CaseFormSet(instance=self.patient,
                             data=data)

    def dispatch(self, request, pk):
        self.patient = get_object_or_404(Patient,
                                        id=pk,
                                        owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'patient': self.patient,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        pdb.set_trace()
        if formset.is_valid():
            formset.save()
            return redirect('manage_patient_list')
        return self.render_to_response({'patient': self.patient,
                                        'formset': formset})
    
    
class PatientListView(TemplateResponseMixin, View):
    model = Patient
    template_name = 'patients/patient/list.html'

    def get(self, request, subject=None):
        #pdb.set_trace()
        subjects = Subject.objects.annotate(
                            total_patients=Count('patients'))
        patients = Patient.objects.annotate(
                           total_cases=Count('cases'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            patients = patients.filter(subject=subject)
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'patients': patients})
    
    
class PatientDetailView(DetailView):
    model = Patient
    template_name = 'patients/patient/detail.html'
    
    
#class CaseCreateView(CreateView):
#    model = Case
#    pdb.set_trace()
#    def form_valid(self, form):
#        pdb.set_trace()
#        return HttpResponseRedirect(self.get_success_url())


#class StudyCreateUpdateView(TemplateResponseMixin, View):
#    case = None
#    model = None
#    obj = None
#    template_name = 'patients/manage/study/form.html'
#
#    def get_model(self, model_name):
#        if model_name in ['text', 'video', 'image', 'file']:
#            return apps.get_model(app_label='patients',
#                                  model_name=model_name)
#        return None
#
#    def get_form(self, model, *args, **kwargs):
#        Form = modelform_factory(model, exclude=['owner',
#                                                 'order',
#                                                 'created',
#                                                 'updated'])
#        return Form(*args, **kwargs)
#
#    def dispatch(self, request, case_id, model_name, id=None):
#        self.case = get_object_or_404(Case,
#                                       id=case_id,
#                                       patient__owner=request.user)
#        self.model = self.get_model(model_name)
#        if id:
#            self.obj = get_object_or_404(self.model,
#                                         id=id,
#                                         owner=request.user)
#        return super().dispatch(request, case_id, model_name, id)
#
#    def get(self, request, case_id, model_name, id=None):
#        form = self.get_form(self.model, instance=self.obj)
#        return self.render_to_response({'form': form,
#                                        'object': self.obj})
#
#    def post(self, request, case_id, model_name, id=None):
#        form = self.get_form(self.model,
#                             instance=self.obj,
#                             data=request.POST,
#                             files=request.FILES)
#        if form.is_valid():
#            obj = form.save(commit=False)
#            obj.owner = request.user
#            obj.save()
#            if not id:
#                # new study
#                Study.objects.create(case=self.case,
#                                       item=obj)
#            return redirect('case_study_list', self.case.id)
#
#        return self.render_to_response({'form': form,
#                                        'object': self.obj})
#
#
#class StudyDeleteView(View):
#    def post(self, request, id):
#        study = get_object_or_404(Study,
#                                    id=id,
#                                    case__patient__owner=request.user)
#        case = study.case
#        study.item.delete()
#        study.delete()
#        return redirect('case_study_list', case.id)
#
#
#class CaseStudyListView(TemplateResponseMixin, View):
#    template_name = 'patients/manage/case/study_list.html'
#
#    def get(self, request, case_id):
#        case = get_object_or_404(Case,
#                                   id=case_id,
#                                   patient__owner=request.user)
#
#        return self.render_to_response({'case': case})




class CaseOrderView(CsrfExemptMixin,
                      JsonRequestResponseMixin,
                      View):
    def post(self, request):
        for id, order in self.request_json.items():
            Case.objects.filter(id=id,
                   patient__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


#class StudyOrderView(CsrfExemptMixin,
#                       JsonRequestResponseMixin,
#                       View):
#    def post(self, request):
#        for id, order in self.request_json.items():
#            Study.objects.filter(id=id,
#                       case__patient__owner=request.user) \
#                       .update(order=order)
#        return self.render_json_response({'saved': 'OK'})
