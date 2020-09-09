from rest_framework import serializers
from ..models import Qualification, DoctorProfile, PatientProfile, GeneralSymptom
from covidUsers.serializers import UserProfileSerializer
from os import path
from settings.base import MEDIA_URL

class QaulificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = "__all__"
    

class DoctorProfileSerializer(serializers.ModelSerializer):
    qualification = QaulificationSerializer()
    doctor = UserProfileSerializer()
    class Meta:
        model = DoctorProfile
        fields = [
            "profile_pic",
            "doctor",
            "speciality",
            "experience",
            "description",
            "qualification",
            "fees",
        ]

    def update(self, instance, validated_data):
        doctor = instance.doctor
        doctorDict = validated_data.get('doctor')
        qualification = instance.qualification
        qualificationDict = validated_data.get('qualification')
        qualification.degree = qualificationDict.get('degree', qualification.degree)
        qualification.institute = qualificationDict.get('institute',qualification.institute)
        instance.speciality = validated_data.get('speciality', instance.speciality)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.description = validated_data.get('description', instance.description)
        instance.fees = validated_data.get('fees', instance.fees)
        doctor.name = doctorDict.get('name', doctor.name)
        doctor.gender = doctorDict.get('gender', doctor.gender)
        doctor.dob = doctorDict.get('dob', doctor.dob)
        doctor.age = doctorDict.get('age', doctor.age)
        doctor.phone = doctorDict.get('phone', doctor.phone)
        doctor.address = doctorDict.get('address', doctor.address)
        doctor.otpVerified = doctorDict.get('otpVerified', doctor.otpVerified)
        doctor.latitude = doctorDict.get('latitude', doctor.latitude)
        doctor.longitude = doctorDict.get('longitude', doctor.longitude)
        if validated_data.get('profile_pic'):
            instance.profile_pic = validated_data.get('profile_pic')
        instance.doctor.save()
        return instance
    
class PatientProfileSerializer(serializers.ModelSerializer):
    patient = UserProfileSerializer()
    class Meta:
        model = PatientProfile
        fields = ['profile_pic','medical_history','patient']
    
    def update(self, instance, validated_data):
        patient = instance.patient
        patientDict = validated_data.get('patient')
        instance.medical_history = validated_data.get('medical_history',instance.medical_history)
        patient.name = patientDict.get('name', patient.name)
        patient.gender = patientDict.get('gender', patient.gender)
        patient.dob = patientDict.get('dob', patient.dob)
        patient.age = patientDict.get('age', patient.age)
        patient.phone = patientDict.get('phone', patient.phone)
        patient.address = patientDict.get('address', patient.address)
        patient.otpVerified = patientDict.get('otpVerified', patient.otpVerified)
        patient.latitude = patientDict.get('latitude', patient.latitude)
        patient.longitude = patientDict.get('longitude', patient.longitude)
        if validated_data.get('profile_pic'):
            instance.profile_pic = validated_data.get('profile_pic',instance.profile_pic)
        instance.patient.save()
        return instance