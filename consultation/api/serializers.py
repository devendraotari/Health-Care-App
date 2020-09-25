from rest_framework import serializers
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
from covidUsers.serializers import UserProfileSerializer
from os import path
from settings.base import MEDIA_URL


class QaulificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ['id','degree','institute']
        # exclude = ["doctor_profile"]


class SpecialityTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialityTag
        fields = "__all__"


class DoctorProfileSerializer(serializers.ModelSerializer):
    doctor_qualification = QaulificationSerializer(many=True)
    speciality = SpecialityTagSerializer()

    class Meta:
        model = DoctorProfile
        fields = [
            "id",
            "profile_pic",
            "speciality",
            "experience",
            "description",
            "doctor_qualification",
            "fees",
        ]

    def update(self, instance, validated_data):
        qualification = instance.qualification
        qualificationDict = validated_data.get("qualification")
        qualification.degree = qualificationDict.get("degree", qualification.degree)
        qualification.institute = qualificationDict.get(
            "institute", qualification.institute
        )
        instance.speciality = validated_data.get("speciality", instance.speciality)
        instance.experience = validated_data.get("experience", instance.experience)
        instance.description = validated_data.get("description", instance.description)
        instance.fees = validated_data.get("fees", instance.fees)

        if validated_data.get("profile_pic"):
            instance.profile_pic = validated_data.get("profile_pic")
        instance.doctor.save()

        return instance


class PatientProfileSerializer(serializers.ModelSerializer):
    # patient = UserProfileSerializer()
    class Meta:
        model = PatientProfile
        fields = ["id", "profile_pic", "medical_history"]

    def update(self, instance, validated_data):

        instance.medical_history = validated_data.get(
            "medical_history", instance.medical_history
        )

        if validated_data.get("profile_pic"):
            instance.profile_pic = validated_data.get(
                "profile_pic", instance.profile_pic
            )
        instance.save()
        return instance


class GeneralSymptomSerializer(serializers.ModelSerializer):
    category = SpecialityTagSerializer()
    class Meta:
        model = GeneralSymptom
        fields = "__all__"

class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = "__all__"

class FileLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileLabel
        fields = "__all__"

class XRayFieldSerializer(serializers.ModelSerializer):
    label = FileLabelSerializer()
    class Meta:
        model = XRayField
        fields = ['xray','label','description','uploaded_by','uploaded_for']