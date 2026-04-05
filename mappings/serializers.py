from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """Serializer for creating/listing patient-doctor mappings."""

    class Meta:
        model = PatientDoctorMapping
        fields = ('id', 'patient', 'doctor', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate(self, data):
        """Ensure the same mapping does not already exist."""
        if PatientDoctorMapping.objects.filter(
            patient=data['patient'],
            doctor=data['doctor'],
        ).exists():
            raise serializers.ValidationError(
                "This doctor is already assigned to this patient."
            )
        return data


class PatientDoctorMappingDetailSerializer(serializers.ModelSerializer):
    """Serializer with nested patient/doctor details for read operations."""

    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ('id', 'patient', 'doctor', 'created_at')
