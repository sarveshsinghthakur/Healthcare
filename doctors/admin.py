from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'specialization', 'license_number', 'created_by')
    search_fields = ('first_name', 'last_name', 'specialization', 'license_number')
    list_filter = ('specialization', 'created_at')
