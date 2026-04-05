from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import PatientDoctorMapping
from .serializers import (
    PatientDoctorMappingSerializer,
    PatientDoctorMappingDetailSerializer,
)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def mapping_list_create(request):
    """
    GET  /api/mappings/  — Retrieve all patient-doctor mappings.
    POST /api/mappings/  — Assign a doctor to a patient.
         Body: { "patient": <patient_id>, "doctor": <doctor_id> }
    """
    if request.method == 'GET':
        mappings = PatientDoctorMapping.objects.all()
        serializer = PatientDoctorMappingDetailSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST
    serializer = PatientDoctorMappingSerializer(data=request.data)
    if serializer.is_valid():
        mapping = serializer.save()
        detail_serializer = PatientDoctorMappingDetailSerializer(mapping)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mapping_by_patient(request, patient_id):
    """
    GET /api/mappings/<patient_id>/  — Get all doctors assigned to a specific patient.
    """
    mappings = PatientDoctorMapping.objects.filter(patient_id=patient_id)
    if not mappings.exists():
        return Response(
            {'message': 'No mappings found for this patient.'},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = PatientDoctorMappingDetailSerializer(mappings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def mapping_delete(request, pk):
    """
    DELETE /api/mappings/<id>/  — Remove a doctor from a patient.
    """
    try:
        mapping = PatientDoctorMapping.objects.get(pk=pk)
    except PatientDoctorMapping.DoesNotExist:
        return Response(
            {'error': 'Mapping not found.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    mapping.delete()
    return Response(
        {'message': 'Mapping deleted successfully.'},
        status=status.HTTP_204_NO_CONTENT,
    )
