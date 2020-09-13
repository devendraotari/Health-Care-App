from django.urls import path
from .views import (
    DoctorProfileListView,
    DoctorProfileDetailView,
    DoctorProfilePublicView,
    PatientProfileDetailView,
    PatientProfileListView,
    PatientProfilePublicView,
    GeneralSymptomsView,
    QualificationDetailsAndUpdateView,
    QualificationCreateView,
)

urlpatterns = [
    path("", DoctorProfileListView.as_view()),
    path("doctor-profiles/", DoctorProfileListView.as_view()),
    path("doctor-public-profile/<int:pk>/", DoctorProfilePublicView.as_view()),
    path("doctor-details/", DoctorProfileDetailView.as_view()),
    path("create-qualification/",QualificationCreateView.as_view()),
    path("qualifications/<int:pk>",QualificationDetailsAndUpdateView.as_view()),
    path("qualifications/",QualificationDetailsAndUpdateView.as_view()),
    path("patient-profiles/", PatientProfileListView.as_view()),
    path("patient-public-profile/<int:pk>", PatientProfilePublicView.as_view()),
    path("patient-details/", PatientProfileDetailView.as_view()),
    path("general-symptoms/",GeneralSymptomsView.as_view()),
    path("general-symptoms/<int:pk>",GeneralSymptomsView.as_view()),
]
