from django.db import models
from .querysets import DoctorProfileQuerySet, XRayFieldQuerySet,QualificationQuerySet

class QualificationManager(models.Manager):
    def get_queryset(self):
        return QualificationQuerySet(self.model, using=self._db)

    def qualifications_by_profile(self,*args, **kwargs):
        return self.get_queryset().qualifications_by_profile(*args, **kwargs)


class DoctorProfileManager(models.Manager):
    def get_queryset(self):
        return DoctorProfileQuerySet(self.model, using=self._db)

    def with_speciality_id(self, speciality_id, *args, **kwargs):
        return self.get_queryset().with_speciality_id(speciality_id, *args, **kwargs)

class XRayFieldManager(models.Manager):
    def get_queryset(self):
        return XRayFieldQuerySet(self.model, using=self._db)

    def all_xrays_by_label(self,*args, **kwargs):
        self.get_queryset().all_xrays_by_label(*args, **kwargs)