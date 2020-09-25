from django.contrib import admin
from .models import (
    Qualification,
    DoctorProfile,
    PatientProfile,
    GeneralSymptom,
    SpecialityTag,
)

admin.site.register(SpecialityTag)
admin.site.register(Qualification)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(GeneralSymptom)
