from django.db.models.signals import post_save
from django.dispatch import receiver
from consultation.models import Consultation, DoctorProfile

@receiver(post_save, sender=Consultation)
def add_patient_to_doctor_profile(sender, instance, created, **kwargs):
    patientObj = instance.symptoms.created_by
    doctorObj = instance.symptoms.assigned_doctor
    doctorObj.doctor.patients.add(patientObj)
    doctorObj.doctor.save()
