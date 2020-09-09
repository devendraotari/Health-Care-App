from django.urls import path
from .views import (
    DoctorProfileListView,
    DoctorProfileDetailView,
    PatientProfileDetailView,
    PatientProfileListView,
)

urlpatterns = [
    path("", DoctorProfileListView.as_view()),
    path("doctor-profiles/", DoctorProfileListView.as_view()),
    path("patient-profiles/", PatientProfileListView.as_view()),
    path("doctor-details/<pk>", DoctorProfileDetailView.as_view()),
    path("patient-details/<pk>", PatientProfileDetailView.as_view()),
]
