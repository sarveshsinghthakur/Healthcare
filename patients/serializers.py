from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient CRUD operations."""

    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Patient
        fields = (
            'id', 'created_by', 'first_name', 'last_name',
            'date_of_birth', 'gender', 'phone', 'email',
            'address', 'medical_history', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
