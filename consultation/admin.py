from django.contrib import admin
from .models import (
    Qualification,
    DoctorProfile,
    PatientProfile,
    GeneralSymptom,
    SpecialityTag,
    Consultation,
    FileLabel,
    XRayField,
)
admin.site.register(Consultation)
admin.site.register(FileLabel)
admin.site.register(XRayField)
admin.site.register(SpecialityTag)
admin.site.register(Qualification)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(GeneralSymptom)
