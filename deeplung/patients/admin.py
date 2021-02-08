from django.contrib import admin
from .models import Subject, Patient, Case


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class CaseInline(admin.StackedInline):
    model = Case


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['surname', 'name', 'created']
    #prepopulated_fields = {'slug': ('title',)}
    inlines = [CaseInline]
