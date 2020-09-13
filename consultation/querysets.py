# from consultation.models import FileLabel
from django.db import models

class QualificationQuerySet(models.QuerySet):
    def qualifications_by_profile(self,*args, **kwargs):
        if 'doctor_profile' in kwargs:
            print("IN query set method")
            result = self.filter(doctor_profile=kwargs['doctor_profile'])
            print(type(result))
            return result
        else:
            return self

class DoctorProfileQuerySet(models.QuerySet):
    def with_speciality_id(self, speciality_id, *args, **kwargs):
        return self.filter(speciality_id=speciality_id)

class XRayFieldQuerySet(models.QuerySet):
    def all_xrays_by_label(self,*args, **kwargs):
        result = None
        try:
            if 'label_name' in kwargs:
                labelObj = FileLabel.objects.all().filter(name=kwargs['label_name']).first()
                result = self.filter(label=labelObj)
            elif args and isinstance(args[0], FileLabel):
                result = self.filter(label=args[0])
            else:
                raise AttributeError
        except Exception as e:
            print("Provide label_name=<name_of_label> as key word arguement")
            print(str(e))
        finally:
            return result
    
    def all_xrays_of_patient(self,patient=None,*args, **kwargs):
        pass
    
    def all_xrays_for_doctor(self,doctor=None,*args, **kwargs):
        pass
