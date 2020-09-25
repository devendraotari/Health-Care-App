from django.shortcuts import render
from django.db import transaction
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import RetrieveModelMixin
from covidUsers.models import CustomUser
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
)
from ..models import (
    Qualification,
    DoctorProfile,
    PatientProfile,
    GeneralSymptom,
    SpecialityTag,
    Consultation,
    XRayField,
    FileLabel,
)
from .serializers import (
    DoctorProfileSerializer,
    PatientProfileSerializer,
    GeneralSymptomSerializer,
    QaulificationSerializer,
    ConsultationSerializer,
    XRayFieldSerializer,
    FileLabelSerializer,
    SpecialityTagSerializer,
)
import traceback
from .utils import get_request_user, create_or_update_symptoms
from consultation.validators import remove_blank_fields


class QualificationCreateView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, *args, **kwargs):
        user = get_request_user(request)
        content = None
        response_status = None
        if user and user.user_role.role == "D":
            doctor_profile = user.doctor
            try:
                with transaction.atomic():
                    degree = request.data.get("degree", None)
                    institute = request.data.get("institute", None)
                    qualification = Qualification(
                        degree=degree,
                        institute=institute,
                        doctor_profile=doctor_profile,
                    )
                    qualification.save()
                    serialized = QaulificationSerializer(qualification)
                    content = {"qualification": serialized.data}
                    response_status = status.HTTP_200_OK
            except Exception as e:
                content = {"Error": str(e)}
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            content = {
                "msg": "Authentication token needed in request headers and user has to be a doctor"
            }
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(content, status=response_status)


class QualificationDetailsAndUpdateView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, pk=None, *args, **kwargs):
        user = get_request_user(request)
        if user and user.user_role.role == "D":
            doctor_profile = user.doctor
            try:
                qualifications = Qualification.objects.all().qualifications_by_profile(
                    doctor_profile=doctor_profile
                )
            except Exception as e:
                return Response({"Error": f"Object does not exists {str(e)}"})
            if pk:
                try:
                    qualifications = qualifications.filter(Q(id=pk))
                except Exception as e:
                    return Response({"Error": f"Object does not exists {str(e)}"})
        serialized = QaulificationSerializer(qualifications, many=True)
        content = {"qualifications": serialized.data}
        return Response(content, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        user = get_request_user(request)
        content = None
        response_status = None
        if user:
            qualification = Qualification.objects.all().filter(id=pk).first()
            if qualification:
                try:
                    with transaction.atomic():
                        qualification.degree = request.data.get(
                            "degree", qualification.degree
                        )
                        qualification.institute = request.data.get(
                            "institute", qualification.institute
                        )
                        qualification.save()
                        serialized = QaulificationSerializer(qualification)
                        content = {"qualification": serialized.data}
                        response_status = status.HTTP_200_OK
                except Exception as e:
                    content = {"Error": str(e)}
                    response_status = status.HTTP_400_BAD_REQUEST
            else:
                content = {"Error": f"No qualification record for Id {pk}"}
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            content = {"msg": "Authentication token needed in request headers"}
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(content, status=response_status)


class DoctorProfileListView(ListAPIView):
    """
    This view will list of all the doctor profile
    mapped with url 'consultation/doctor-profiles/'
    """

    permission_classes = ()
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer


class DoctorConsultedPatientsListView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        user = get_request_user(request)
        if user and user.user_role.role == "D":
            try:
                patientObj = (
                    CustomUser.objects.all()
                    .filter(created_by_patient__assigned_doctor_id=user.id)
                    .select_related("patient")
                )
                patient_profiles = []
                for po in patientObj:
                    patient_profiles.append(po.patient)
                serialized = PatientProfileSerializer(patient_profiles, many=True)
                return Response(
                    {"patient_profiles": serialized.data}, status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"msg": "Authentication token needed in request headers"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DoctorProfileDetailView(APIView):
    """
    This view will provide the detail doctor profile
    mapped with url 'consultation/doctor-details//'
    """

    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        user = get_request_user(request)
        if user and user.user_role.role == "D":
            doctor_profile = (
                DoctorProfile.objects.all()
                .filter(doctor_id=user.id)
                .prefetch_related("doctor_qualification", "speciality")
                .first()
            )
            serialized = DoctorProfileSerializer(doctor_profile)
            content = {"doctor_profile": serialized.data}
            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response(
                {"msg": "Authentication token needed in request headers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request):
        user = get_request_user(request)
        request = remove_blank_fields(request)
        validated_data = request.data
        if user and validated_data:
            doctor_profile = (
                DoctorProfile.objects.all()
                .filter(doctor_id=user.id)
                .prefetch_related("doctor_qualification", "speciality")
                .first()
            )
            with transaction.atomic():
                qualificationDict = validated_data.get("doctor_qualification", None)
                if qualificationDict:
                    qualification = doctor_profile.doctor_qualification
                    qualification.degree = qualificationDict.get(
                        "degree", qualification.degree
                    )
                    qualification.institute = qualificationDict.get(
                        "institute", qualification.institute
                    )
                specialityDict = validated_data.get("speciality", None)
                if specialityDict:
                    speciality = doctor_profile.speciality
                    doctor_profile.speciality = validated_data.get(
                        "speciality", speciality
                    )
                doctor_profile.experience = validated_data.get(
                    "experience", doctor_profile.experience
                )
                doctor_profile.description = validated_data.get(
                    "description", doctor_profile.description
                )
                doctor_profile.fees = validated_data.get("fees", doctor_profile.fees)
                doctor_profile.save()
                serialized = DoctorProfileSerializer(doctor_profile)
            return Response(
                {
                    "msg": "Doctor profile Updated successfully",
                    "doctor_profile": serialized.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"msg": "Authentication token needed in request headers"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DoctorProfilePublicView(RetrieveAPIView):
    permission_classes = ()
    authentication_classes = []
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer


"""
Patient profile Related views starts from here
"""


class PatientProfileListView(ListAPIView):
    permission_classes = ()
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer


class PatientProfileDetailView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, *args, **kwargs):
        user = get_request_user(request)
        if user:
            patient_profile = (
                PatientProfile.objects.all().filter(patient_id=user.id).first()
            )
            serialized = PatientProfileSerializer(patient_profile)
            content = {"patient_profile": serialized.data}
            return Response(content)
        else:
            return Response(
                {"msg": "Authentication token needed in request headers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request):
        user = get_request_user(request)
        request = remove_blank_fields(request)
        new_data = request.data
        # print(user.user_role)
        if user and user.user_role.role == "P":
            try:
                with transaction.atomic():
                    patient_profile = (
                        PatientProfile.objects.all().filter(patient_id=user.id).first()
                    )
                    patient_profile.profile_pic = new_data.get(
                        "profile_pic", patient_profile.profile_pic
                    )
                    patient_profile.medical_history = new_data.get(
                        "medical_history", patient_profile.medical_history
                    )
                    patient_profile.save()
                    serialized_profile = PatientProfileSerializer(patient_profile)
                    response = {"patient_profile": serialized_profile.data}
                    return Response(response, status=status.HTTP_201_CREATED)
            except Exception as e:
                traceback.print_exc()
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"msg": "Authentication token needed in request headers"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PatientProfilePublicView(RetrieveAPIView):
    permission_classes = ()
    authentication_classes = []
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer


"""
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
General Symptoms related views starts from here
/////////////////////////////////////////////////////////////////////
"""


class GeneralSymptomsView(APIView, RetrieveModelMixin):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]
    queryset = GeneralSymptom.objects.all()
    serializer_class = GeneralSymptomSerializer

    def get_object(self, request, pk):
        context = {
            "msg": "General symptoms form is created successfully",
            "general_symtopms id": pk,
        }
        return Response(context)

    def get(self, request, pk=None):
        user = get_request_user(request)
        if user:
            if pk:
                general_symtopms_data = GeneralSymptom.objects.all().filter(
                    Q(id=pk) & Q(created_by=user.id) | Q(assigned_doctor=user.id)
                )
            else:
                general_symtopms_data = GeneralSymptom.objects.all().filter(
                    Q(created_by=user.id) | Q(assigned_doctor=user.id)
                )
            serialized_data = GeneralSymptomSerializer(general_symtopms_data, many=True)
            return Response({"general_symtopms_data": serialized_data.data})
        else:
            return Response(
                {"msg": "Authentication token needed in request headers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request):
        user = get_request_user(request)
        context = None
        response_status = None
        if user and user.user_role.role == "P":
            request = remove_blank_fields(request)
            resultDict = create_or_update_symptoms(user=user, request=request)
            print(resultDict)
            try:
                with transaction.atomic():
                    general_symptom = resultDict.get("general_symptom", None)
                    if general_symptom:
                        general_symptom.save()
                        serialized_data = GeneralSymptomSerializer(general_symptom)
                        context = {
                            "msg": "General symptoms form is created successfully",
                            "general_symtopm": serialized_data.data,
                        }
                        response_status = status.HTTP_200_OK
                    else:
                        context = resultDict
                        response_status = status.HTTP_400_BAD_REQUEST
                    return Response(context, status=response_status)

            except Exception as e:
                return Response(
                    {
                        "msg": "database operation failed",
                        "Error": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            print(user.user_role)
            return Response(
                {
                    "msg": "Authentication token needed in request headers and user must be a patient"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request, pk, *args, **kwargs):
        user = get_request_user(request)
        content = None
        response_status = None
        if user and user.user_role.role == "P":
            try:
                with transaction.atomic():
                    resultDict = create_or_update_symptoms(
                        pk, user=user, request=request
                    )
                    general_symptom = resultDict.get("general_symptom", None)
                    if general_symptom:
                        general_symptom.save()
                        serialized = GeneralSymptomSerializer(general_symptom)
                        content = {"general_symptom": serialized.data}
                        response_status = status.HTTP_200_OK
                    else:
                        content = resultDict
                        response_status = status.HTTP_400_BAD_REQUEST
            except Exception as e:
                content = {"Error": str(e)}
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            content = {
                "msg": "Only Authenticated users having patient permissions can update symtopms data",
                "general_symtopms id": pk,
            }
            response_status = status.HTTP_403_FORBIDDEN
        return Response(content, status=response_status)


"""
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    Consultation related views starts here
////////////////////////////////////////////////////////////////////
"""


class ConsultationsView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]
    # queryset = Consultation.objects.all()
    # serializer_class = ConsultationSerializer

    def get(self, request, pk=None):
        user = get_request_user(request)
        consultations = None
        if user:
            if pk:
                consultations = Consultation.objects.by_user_id(user.id).filter(
                    Q(id=pk)
                )
            else:
                consultations = Consultation.objects.by_user_id(user.id)
                print(type(consultations))
            serialized_data = ConsultationSerializer(consultations, many=True)
            return Response({"consultation_data": serialized_data.data})
        else:
            return Response(
                {"msg": "Authentication token needed in request headers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request, pk):
        user = get_request_user(request)
        consultation = None
        if user:
            consultation = (
                Consultation.objects.by_user_id(user.id).filter(Q(id=pk)).first()
            )
            consultation.Note = request.data.get("note", consultation.Note)
            consultation.prescription_text = request.data.get(
                "prescription", consultation.prescription_text
            )
            if not request.data.get("prescription") == " ":
                consultation.prescription = request.data.get(
                    "prescription", consultation.prescription
                )
            consultation.save()
            serialized_data = ConsultationSerializer(consultation)
            return Response({"consultation_data": serialized_data.data})
        else:
            return Response(
                {"msg": "Authentication token needed in request headers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request, *args, **kwargs):
        user = get_request_user(request)
        request = remove_blank_fields(request)
        validated_data = request.data
        consultation = None
        if user and user.user_role.role == "D":
            if "symptom_id" in validated_data:
                symptom_id = validated_data.get("symptom_id")
                try:
                    symptomObj = (
                        GeneralSymptom.objects.all()
                        .filter(Q(assigned_doctor=user.id) and Q(id=symptom_id))
                        .first()
                    )
                    consultation = Consultation(symptoms=symptomObj)
                    consultation.Note = validated_data.get("note", consultation.Note)
                    consultation.prescription_text = validated_data.get(
                        "prescription_text", consultation.prescription_text
                    )
                    consultation.prescription = validated_data.get(
                        "prescription", consultation.prescription
                    )
                    consultation.save()
                    serialized_data = ConsultationSerializer(consultation)
                    return Response({"consultation_data": serialized_data.data})
                except Exception as e:
                    print(str(e))
                    return Response({"Error": str(e)})
            else:
                return Response({"Error": "Required symptoms_id in request data"})
        else:
            return Response(
                {"msg": "Authentication token needed in request headers"},
                status=status.HTTP_400_BAD_REQUEST,
            )


"""            
 \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
   XRays and File Label Related views
 /////////////////////////////////////////////
"""


class XRayUploadView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self,request,pk=None):
        user = get_request_user(request)
        context, response_status = (None, None)
        request = remove_blank_fields(request)
        if user and user.user_role.role == "D":
            xrayfields = XRayField.objects.filter()
        elif user and user.user_role.role == "P":
            pass
        else:
            return Response(
                {"msg": "Authentication token needed in request headers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request):
        user = get_request_user(request)
        context, response_status = (None, None)
        request = remove_blank_fields(request)
        if user and user.user_role.role == "P":
            xray = request.data.get("xray", None)
            uploaded_for_id = request.data.get("uploaded_for_id", None)
            if xray and uploaded_for_id:
                description = request.data.get("description", None)
                try:
                    uploaded_for = CustomUser.objects.get(id=uploaded_for_id)
                    xray_field = XRayField(
                        xray=xray,
                        uploaded_by=user,
                        uploaded_for=uploaded_for,
                        description=description,
                    )
                    xray_field.save()
                    serialized = XRayFieldSerializer(xray_field)
                    context = {
                        "msg": "XRay has been uploaded successfully",
                        "XRay": serialized.data,
                    }
                    response_status = status.HTTP_200_OK
                except Exception as e:
                    response_status = status.HTTP_400_BAD_REQUEST
                    context = {"Error": f"database error {str(e)}"}
            else:
                response_status = status.HTTP_400_BAD_REQUEST
                context = {"Error": "Missing file or uploaded for id in request data"}
        else:
            response_status = status.HTTP_403_FORBIDDEN
            context = {
                "Error": "Authentication Needed and user must be a Patient to upload a XRay"
            }
        return Response(context, response_status)

    def put(self, request, pk):
        context, response_status = (None, None)
        xray_field = None
        user = get_request_user(request)
        role = user.user_role.role

        try:
            xray_field = XRayField.objects.select_related(
                "label", "uploaded_by", "uploaded_for"
            ).get(id=pk)
        except Exception as e:
            response_status = status.HTTP_403_FORBIDDEN
            context = {
                "Error": f"Object does not found for pk {pk} \n Database error {str(e)}"
            }
            return Response(context, response_status)
        if user and role == "D" and user.id == xray_field.uploaded_for.id:
            with transaction.atomic():
                label_name = request.data.get("label_name", None)
                description = request.data.get("description", None)
                file_label = FileLabel(name=label_name, description=description)
                file_label.save()
                xray_field.label = file_label
                xray_field.save()
        elif user and role == "P" and user.id == xray_field.uploaded_by.id:
            with transaction.atomic():
                request = remove_blank_fields(request)
                new_xray = request.data.get("xray_file", xray_field.xray)
                xray_field.xray = new_xray
                xray_field.save()
        else:
            response_status = status.HTTP_403_FORBIDDEN
            context = {
                "Error": "Authentication Needed and user must be a Patient to upload a XRay"
            }
        return Response(context, response_status)

    def delete(self, request, pk):
        context, response_status = (None, None)
        user = get_request_user(request)
        try:
            xray_field = XRayField.objects.select_related("uploaded_by, label").get(
                id=pk
            )
            context = {"msg": f"XRayField with id {pk} has been deleted successfully"}
            response_status = status.HTTP_200_OK
        except Exception as e:
            context = {"Error": f"Database error {str(e)}"}
            response_status = status.HTTP_404_NOT_FOUND
            return Response(context, response_status)
        if user and user.user_role.role == "P" and user.id == xray_field.uploaded_by.id:
            xray_field.delete()
        else:
            response_status = status.HTTP_403_FORBIDDEN
            context = {
                "Error": "Authentication Needed and user must be a Patient"
            }
        return Response(context, response_status)
