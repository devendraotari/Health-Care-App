from django.shortcuts import render
from django.db import transaction
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
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from ..models import DoctorProfile, PatientProfile, GeneralSymptom, Qualification
from .serializers import (
    DoctorProfileSerializer,
    PatientProfileSerializer,
    GeneralSymptomSerializer,
    QaulificationSerializer,
)
import traceback
from .utils import get_request_user, create_or_update_symptoms

class QualificationCreateView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def post(self,request,*args, **kwargs):
        user = get_request_user(request)
        content = None
        response_status = None
        if user:
            doctor_profile = user.doctor
            try :
                with transaction.atomic():
                    degree = request.data.get('degree',None)
                    institute = request.data.get('institute',None)
                    qualification = Qualification(degree=degree,institute=institute,doctor_profile=doctor_profile)
                    qualification.save()
                    serialized = QaulificationSerializer(qualification)
                    content = {"qualification":serialized.data}
                    response_status = status.HTTP_200_OK
            except Exception as e:
                content = {"Error":str(e)}
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            content = {"msg": "Authentication token needed in request headers"}
            response_status=status.HTTP_400_BAD_REQUEST

        return Response(content,status=response_status)


class QualificationDetailsAndUpdateView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request,pk=None ,*args, **kwargs):
        user = get_request_user(request)
        print(f"$$$$$$#######{pk}")
        doctor_profile = user.doctor
        qualifications = Qualification.objects.all().qualifications_by_profile(
            doctor_profile=doctor_profile
        )
        serialized = QaulificationSerializer(qualifications,many=True)
        content = {"qualifications": serialized.data}
        return Response(content, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        user = get_request_user(request)
        content = None
        response_status = None
        if user:
            qualification = Qualification.objects.all().filter(id=pk).first()
            if qualification:
                try :
                    with transaction.atomic():
                        qualification.degree = request.data.get('degree',qualification.degree)
                        qualification.institute = request.data.get('institute',qualification.institute)
                        qualification.save()
                        serialized = QaulificationSerializer(qualification)
                        content = {"qualification":serialized.data}
                        response_status = status.HTTP_200_OK
                except Exception as e:
                    content = {"Error":str(e)}
                    response_status = status.HTTP_400_BAD_REQUEST
            else:
                content = {"Error":f"No qualification record for Id {pk}"}
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            content = {"msg": "Authentication token needed in request headers"}
            response_status=status.HTTP_400_BAD_REQUEST

        return Response(content, status=response_status)
    

class DoctorProfileListView(ListAPIView):
    """
    This view will list of all the doctor profile
    mapped with url 'consultation/doctor-profiles/'
    """

    permission_classes = ()
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer


class DoctorProfileDetailView(APIView):
    """
    This view will provide the detail doctor profile
    mapped with url 'consultation/doctor-details//'
    """

    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        user = get_request_user(request)
        if user:
            doctor_profile = (
                DoctorProfile.objects.all().filter(doctor_id=user.id).first()
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
        validated_data = request.data
        if user and validated_data:
            doctor_profile = (
                DoctorProfile.objects.all().filter(doctor_id=user.id).first()
            )
            with transaction.atomic():
                qualification = doctor_profile.qualification
                qualificationDict = validated_data.get("qualification")
                qualification.degree = qualificationDict.get(
                    "degree", qualification.degree
                )
                qualification.institute = qualificationDict.get(
                    "institute", qualification.institute
                )
                doctor_profile.speciality = validated_data.get(
                    "speciality", doctor_profile.speciality
                )
                doctor_profile.experience = validated_data.get(
                    "experience", doctor_profile.experience
                )
                doctor_profile.description = validated_data.get(
                    "description", doctor_profile.description
                )
                doctor_profile.fees = validated_data.get("fees", doctor_profile.fees)
                doctor_profile.save()
            return Response(
                {"msg": "Doctor profile Updated successfully"},
                status=status.HTTP_200_SUCCESS,
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
        new_data = request.data
        if user:
            try:
                with transaction.atomic():
                    patient_profile = (
                        PatientProfile.objects.all().filter(patient_id=user.id).first()
                    )
                    patient_profile.profile_pic = new_data.get(
                        "profile_pic", patient_profile.profile_pic
                    )
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

    def get(self, request, pk):
        user = get_request_user(request)
        if user:
            general_symtopms_data = GeneralSymptom.objects.all().filter(
                created_by=user.id
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
        assigned_doctor = None
        if user and user.user_role.role == "P":
            assigned_doctor_id = request.data.get("assigned_doctor_id", None)
            if assigned_doctor_id:
                assigned_doctor = CustomUser.objects.all().filter(id=assigned_doctor_id)
            else:
                return Response({"msg": "Please provide doctor Id "})
            try:
                with transaction.atomic():
                    general_symptom = create_or_update_symptoms(
                        user=user, assigned_doctor=assigned_doctor, request=request
                    )
                    general_symptom.save()
                    serialized_data = GeneralSymptomSerializer(general_symptom)
                    context = {
                        "msg": "General symptoms form is created successfully",
                        "general_symtopms": serialized_data.data,
                    }
                return Response(context,status=status.HTTP_200_OK)

            except Exception as e:
                return Response(
                    {
                        "msg": "database operation failed",
                        "Error": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"msg": "Authentication token needed in request headers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request, pk, *args, **kwargs):
        user = get_request_user(request)
        context = {
            "msg": "General symptoms form is created successfully",
            "general_symtopms id": pk,
        }
        return Response(context)
