from django.core.management.base import BaseCommand
from consultation.models import (
    Qualification,
    DoctorProfile,
    PatientProfile,
    GeneralSymptom,
    Consultation,
    XRayField,
    FileLabel,
    SpecialityTag,
    QUALIFICATION_CHOICES,
)
from covidUsers.models import CustomUser,Role,ROLE_CHOICES

class Command(BaseCommand):

    help = """Creates Four roles Doctor, Patient, Counsellor and Other 
            these roles will be used while creating CustomUsers"""
    


    def create_and_assign_qualifications(self):
        dprofiles = DoctorProfile.objects.all()
        for dp in dprofiles:
            print(type(dp))
            qualification = Qualification(degree=QUALIFICATION_CHOICES[0][0],doctor=dp)
            qualification.save()
    
    def create_speciality_tags(self):
        dprofiles = DoctorProfile.objects.all()
        st = SpecialityTag(tag_name="General Physician",description="General Physician")
        st.save()
        for profile in dprofiles:
            profile.speciality = st
            profile.save()

    def create_general_symtopms(self):
        doctor = CustomUser.objects.all().filter(user_role_id=1).first()
        patients = CustomUser.objects.all().filter(user_role_id=3)
        category = SpecialityTag.objects.all().first()
        for patient in patients:
            gs = GeneralSymptom(created_by=patient,assigned_doctor=doctor,category=category)
            gs.save()

    def create_consultations(self):
        for gs in GeneralSymptom.objects.all():
            cs = Consultation(symptoms=gs)
            cs.save()
    
    def create_file_labels(self):
        fl = FileLabel(name="shoulder",description="this label is for shoulder related data files")
        fl.save()

    def add_arguments(self, parser):
        parser.add_argument(
            "--all", help="Takes no argument creates all roles by default"
        )

    def handle(self, *args, **kwargs):
        if not GeneralSymptom.objects.all():
            self.create_speciality_tags()
            self.create_and_assign_qualifications()
            self.create_file_labels()
            self.create_general_symtopms()
            self.create_consultations()
            self.stdout.write(self.style.SUCCESS('All database is populated and saved successfully.'))
        else:
            self.stdout.write(self.style.FAILED('Database Needs to be completely empty.'))