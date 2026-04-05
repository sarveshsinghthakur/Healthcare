from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Doctor
from .serializers import DoctorSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def doctor_list_create(request):
    """
    GET  /api/doctors/  — Retrieve all doctors.
    POST /api/doctors/  — Add a new doctor (authenticated users only).
    """
    if request.method == 'GET':
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST
    serializer = DoctorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def doctor_detail(request, pk):
    """
    GET    /api/doctors/<id>/  — Get details of a specific doctor.
    PUT    /api/doctors/<id>/  — Update doctor details.
    DELETE /api/doctors/<id>/  — Delete a doctor record.
    """
    try:
        doctor = Doctor.objects.get(pk=pk)
    except Doctor.DoesNotExist:
        return Response(
            {'error': 'Doctor not found.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == 'GET':
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    doctor.delete()
    return Response(
        {'message': 'Doctor deleted successfully.'},
        status=status.HTTP_204_NO_CONTENT,
    )
