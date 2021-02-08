from django.urls import path
from . import views

urlpatterns = [
    path('mine/',
         views.ManagePatientListView.as_view(),
         name='manage_patient_list'),

    path('create/',
         views.PatientCreateView.as_view(),
         name='patient_create'),

    path('<pk>/edit/',
         views.PatientUpdateView.as_view(),
         name='patient_edit'),

    path('<pk>/delete/',
         views.PatientDeleteView.as_view(),
         name='patient_delete'),
         
    path('<pk>/case/',
     views.PatientCaseUpdateView.as_view(),
     name='patient_case_update'),

    path('case/<int:case_id>/study/<model_name>/create/',
         views.StudyCreateUpdateView.as_view(),
         name='case_study_create'),

    path('case/<int:case_id>/study/<model_name>/<id>/',
         views.StudyCreateUpdateView.as_view(),
         name='case_study_update'),

    path('study/<int:id>/delete/',
         views.StudyDeleteView.as_view(),
         name='case_study_delete'),

    path('case/<int:case_id>/',
         views.CaseStudyListView.as_view(),
         name='case_study_list'),

    path('case/order/',
         views.CaseOrderView.as_view(),
         name='case_order'),

     path('study/order/',
          views.StudyOrderView.as_view(),
          name='study_order'),
    
    path('subject/<slug:subject>/',
          views.PatientListView.as_view(),
          name='patient_list_subject'),
    
    path('<str:surname>/',
          views.PatientDetailView.as_view(),
          name='patient_detail'),
]
