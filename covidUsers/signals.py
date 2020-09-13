from django.db.models.signals import post_save
from .models import CustomUser, Role, ROLE_CHOICES
from django.dispatch import receiver
from consultation.models import (
    DoctorProfile,
    PatientProfile,
    Qualification,
    QUALIFICATION_CHOICES,
)

# from .utils import is_doctor, is_patient,create_doctor_profile, create_patient_profile


def is_doctor(instance):
    if instance.user_role.role == ROLE_CHOICES[0][0]:
        print("Doctor profile will be created")
        return True
    else:
        return False


def is_patient(instance):
    if instance.user_role.role == ROLE_CHOICES[2][0]:
        print("Patient profile will be created")
        return True
    else:
        return False


def create_doctor_profile(instance):
    if is_doctor(instance):
        # qualification = Qualification()
        # qualification.save()
        profile = DoctorProfile.objects.create(doctor=instance)
        return profile
    else:
        return None


def create_patient_profile(instance):
    if is_patient(instance):
        profile = PatientProfile.objects.create(patient=instance)
        return profile
    else:
        return None


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    print('********create profile -- SIGNAL*******')
    if created:
        if is_doctor(instance):
            create_doctor_profile(instance)
        if is_patient(instance):
            create_patient_profile(instance)


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    if is_doctor(instance):
        instance.doctor.save()
    if is_patient(instance):
        instance.patient.save()
