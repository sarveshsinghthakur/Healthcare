from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'created_by')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('gender', 'created_at')
