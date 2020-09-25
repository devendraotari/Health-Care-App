from django.urls import path
from .views import (
    DoctorProfileListView,
    DoctorProfileDetailView,
    DoctorProfilePublicView,
    DoctorConsultedPatientsListView,
    PatientProfileDetailView,
    PatientProfileListView,
    PatientProfilePublicView,
    GeneralSymptomsView,
    QualificationDetailsAndUpdateView,
    QualificationCreateView,
    ConsultationsView,
    XRayUploadView,
)

urlpatterns = [
    path("doctor-profiles/", DoctorProfileListView.as_view()),
    # for showing doctor profile to patient using profile Id
    path("doctor-public-profile/<int:pk>/", DoctorProfilePublicView.as_view()),
    # for create and update doctor profile details
    path("doctor-details/", DoctorProfileDetailView.as_view()),
    path("doctor-consulted-patients/",DoctorConsultedPatientsListView.as_view()),
    # create qualification data only for doctor type
    path("create-qualification/",QualificationCreateView.as_view()),
    # get and update qualification details of a doctor (pk => qualification id)
    path("qualifications/<int:pk>",QualificationDetailsAndUpdateView.as_view()),
    # all qualification data of a perticular doctor profile 
    path("qualifications/",QualificationDetailsAndUpdateView.as_view()),
    # Detail view of patient profile for doctor to look into
    path("patient-public-profile/<int:pk>", PatientProfilePublicView.as_view()),
    # detail view for patient to edit info
    path("patient-details/", PatientProfileDetailView.as_view()),
    # All general symtopms data of logged in user doctor or patient
    path("general-symptoms/",GeneralSymptomsView.as_view()),
    # update data for patient only and for doctor and patient to Get detail view of general symptom data 
    path("general-symptoms/<int:pk>",GeneralSymptomsView.as_view()),
    # create consultation data for perticular symtopms data and only for doctor 
    path("create-consultation/",ConsultationsView.as_view()),
    # consultation data of logged in user
    path("consultations-data/",ConsultationsView.as_view()),
    # Update consultation by ID for doctor and get details
    path("consultations-data/<int:pk>",ConsultationsView.as_view()),
    # --------------- ^ Tested ^     -------- 
    path("xrayupload/",XRayUploadView.as_view()),
]
