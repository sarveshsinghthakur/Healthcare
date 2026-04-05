from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Patient
from .serializers import PatientSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def patient_list_create(request):
    """
    GET  /api/patients/  — List all patients created by the authenticated user.
    POST /api/patients/  — Create a new patient record.
    """
    if request.method == 'GET':
        patients = Patient.objects.filter(created_by=request.user)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def patient_detail(request, pk):
    """
    GET    /api/patients/<id>/  — Retrieve a patient.
    PUT    /api/patients/<id>/  — Update a patient.
    DELETE /api/patients/<id>/  — Delete a patient.
    """
    try:
        patient = Patient.objects.get(pk=pk, created_by=request.user)
    except Patient.DoesNotExist:
        return Response(
            {'error': 'Patient not found.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    patient.delete()
    return Response(
        {'message': 'Patient deleted successfully.'},
        status=status.HTTP_204_NO_CONTENT,
    )
