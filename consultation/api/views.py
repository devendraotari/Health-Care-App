from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from ..models import DoctorProfile, PatientProfile
from .serializers import DoctorProfileSerializer, PatientProfileSerializer

class DoctorProfileListView(APIView):
    permission_classes = ()
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer

class DoctorProfileDetailView(RetrieveUpdateAPIView):
    permission_classes = ()
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer

class PatientProfileListView(ListAPIView):
    permission_classes = ()
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer

class PatientProfileDetailView(RetrieveUpdateAPIView):
    permission_classes = ()
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer



