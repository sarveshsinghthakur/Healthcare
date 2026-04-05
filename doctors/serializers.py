from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor CRUD operations."""

    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Doctor
        fields = (
            'id', 'created_by', 'first_name', 'last_name',
            'specialization', 'license_number', 'phone', 'email',
            'address', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
