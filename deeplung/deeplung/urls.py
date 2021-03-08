from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from patients.views import PatientListView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('patient/', include('patients.urls')),
    path('', PatientListView.as_view(), name='patient_list'),
    path('api/', include('patients.api.urls', namespace='api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)