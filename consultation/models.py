from django.db import models
from django.urls import reverse
from covidUsers.models import CustomUser
from .managers import QualificationManager,ConsultationManager
# SPECIALITY_CHOICES = (
#     ("cardiac", "Cardiologist"),
#     ("ENT", "ENT specialist"),
#     ("gastrologist", "stomach and digestion"),
#     ("pediatrics", "pediatrics"),
#     ("dermatology", "skin specialist"),
#     ("dentist", "dentist"),
# )

QUALIFICATION_CHOICES = (
    ("MBBS", "MBBS"),
    ("BMBS", "BMBS"),
    ("MBChB", "MBChB"),
    ("MBBCh", "MBBCh"),
    ("MD", "MD"),
    ("Dr.MuD", "Dr.MuD"),
    ("Dr.Med", "Dr.Med"),
    ("DO", "DO"),
    ("PhD", "PhD"),
    ("DPhil", "DPhil"),
    ("MCM", "MCM"),
    ("MS", "MS"),
    ("MPhil", "MPhil"),
    ("DMedSc", "DMedSc"),
    ("DMSc", "DMSc"),
    ("DS", "DS"),
    ("DSurg", "DSurg"),
)


class SpecialityTag(models.Model):
    tag_name = models.CharField(default="",unique=True,null=True, blank=True, max_length=20)
    description = models.CharField(default="", null=True, blank=True, max_length=150)

    class Meta:
        verbose_name = "SpecialityTag"
        verbose_name_plural = "SpecialityTags"

    def __str__(self):
        return self.tag_name

    def get_absolute_url(self):
        return reverse("SpecialityTag_detail", kwargs={"pk": self.pk})


class DoctorProfile(models.Model):
    """
    This class will store info for doctor which will be visible to
    patients. Doctor can edit this profile info and manage what to show
    to patients who want to consult with him.
    """

    profile_pic = models.ImageField(
        default="default.jpg", upload_to="profile_pics", null=True, blank=True
    )
    doctor = models.OneToOneField(
        CustomUser,
        verbose_name="customUser",
        on_delete=models.CASCADE,
        related_name="doctor",
    )
    # patients with whom doctor has consulted with
    patients = models.ManyToManyField(
        CustomUser,
        verbose_name="patients",
        related_name="patients",
    )
    speciality = models.ForeignKey(
        SpecialityTag,
        verbose_name="speciality_tag",
        related_name="doctor_profile",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    experience = models.IntegerField(default=0, blank=True, null=True)
    description = models.TextField(default="", blank=True, null=True)

    fees = models.FloatField(blank=True, null=True, verbose_name="fees")

    class Meta:
        verbose_name = "DoctorProfile"
        verbose_name_plural = "DoctorProfiles"
        ordering = ["-experience"]

    def __str__(self):
        return f"{self.doctor.name} speciality {self.speciality}"

    def get_absolute_url(self):
        return reverse("DoctorProfile_detail", kwargs={"pk": self.pk})


class Qualification(models.Model):
    degree = models.CharField(
        choices=QUALIFICATION_CHOICES, null=True, blank=True, max_length=50
    )
    institute = models.CharField(default="", null=True, blank=True, max_length=50)
    doctor_profile = models.ForeignKey(
        DoctorProfile,
        verbose_name="doctor_profile",
        related_name="doctor_qualification",
        on_delete=models.CASCADE,
    )
    objects = QualificationManager()
    class Meta:
        verbose_name = "Qualification"
        verbose_name_plural = "Qualifications"

    def __str__(self):
        return f"{self.degree} from {self.institute}"

    def get_absolute_url(self):
        return reverse("Qualification_detail", kwargs={"pk": self.pk})

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/
#  Patient Related Models
# //////////////////////////////////////////////////////////////\
class PatientProfile(models.Model):
    """
    this class will store profile info for patient which will be
    visible to doctors.
    """

    profile_pic = models.ImageField(
        default="default.jpg", upload_to="profile_pics", null=True, blank=True
    )
    patient = models.OneToOneField(
        CustomUser,
        verbose_name="customUser",
        on_delete=models.CASCADE,
        related_name="patient",
    )
    medical_history = models.TextField(default="", null=True, blank=True)
    '''
    Fields to add in This model
    • Present Complains:
    • Surgical History:

    • Family History: (Patient has any history of life style diseases in his/her family)

    • Which all treatments have you taken previously? :

    • What all medicines are you taking presently? :

    • Do you have any allergy to specific medicines? :
    '''
    class Meta:
        verbose_name = "PatientProfile"
        verbose_name_plural = "PatientProfiles"

    def __str__(self):
        return "Patient Name" + self.patient.username

    def get_absolute_url(self):
        return reverse("PatientProfile_detail", kwargs={"pk": self.pk})


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#  Symptoms data related Models
# /////////////////////////////////////////////////////


# ----------------------------------------------------------------------------
# Blood pressure: _ / __ (Numeric) mm of Hg (Systolic/Diastolic)
# Blood glucose: __ (Numeric)
# Heart rate: __ (Numeric)
# ECG: _______ (Alphanumeric & Image Upload) (Report Attached)
# Temp: __ (Numeric)
# Pulse: __  (numeric)
# Oxygen saturation: ___  % (Numeric)
# Weight: ___ (Numeric) (kg
# Nutrition / diet diary:  __ (Text) (Report format attached)
# Hearing / audiometry:  __ (Alphanumeric) (Report Attached)
# Retinal scan: ___ (Alphanumeric)
# Optometry: __ (Alphanumeric)
# -----------------------------------------------------------------------------


class GeneralSymptom(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser,
        verbose_name="patient",
        related_name="created_by_patient",
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        SpecialityTag,
        related_name="symptoms_category",
        verbose_name="category",
        on_delete=models.CASCADE,
    )
    assigned_doctor = models.ForeignKey(
        CustomUser,
        default=0,
        verbose_name="doctor",
        related_name="assigned_doctor",
        on_delete=models.SET_DEFAULT,
    )
    systolic = models.FloatField(
        blank=True, null=True, verbose_name="systolic_blood_pressure"
    )
    diatolic = models.FloatField(
        blank=True, null=True, verbose_name="diastolic_blood_pressure"
    )
    blood_glucose = models.FloatField(
        blank=True, null=True, verbose_name="blood_glucose"
    )
    heart_rate = models.FloatField(blank=True, null=True, verbose_name="heart_rate")
    ecg = models.CharField(
        blank=True, null=True, verbose_name="ecg_data", max_length=50
    )
    ecg_report = models.FileField(upload_to="ecg_reports/",blank=True,null=True)
    temp = models.FloatField(blank=True, null=True, verbose_name="temperature")
    pulse = models.FloatField(blank=True, null=True, verbose_name="pulse")
    spo2 = models.FloatField(blank=True, null=True, verbose_name="oxygen_saturation")
    weight = models.FloatField(blank=True, null=True, verbose_name="weight")
    nutrition = models.TextField(default="", blank=True, null=True)
    nutrition_report = models.FileField(upload_to="nutrition_reports/",blank=True,null=True)
    audiometry = models.FloatField(
        blank=True, null=True, verbose_name="autiometry_value"
    )
    audiometry_report = models.FileField(upload_to="audiometry_reports/",blank=True,null=True)
    retina_scan = models.FloatField(blank=True, null=True, verbose_name="retina_scan")
    optometry = models.FloatField(blank=True, null=True, verbose_name="optometry")


    class Meta:
        verbose_name = "GeneralSymptom"
        verbose_name_plural = "GeneralSymptoms"

    def __str__(self):
        return "created by "+ self.created_by.username

    def get_absolute_url(self):
        return reverse("GeneralSymptom_detail", kwargs={"pk": self.pk})


class FileLabel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(
        verbose_name="label_name",blank=False, null=False, max_length=50
    )
    description = models.TextField(
        verbose_name="description", blank=True, null=True, max_length=150
    )

    class Meta:
        verbose_name = "FileLabel"
        verbose_name_plural = "FileLabels"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("FileLabel_detail", kwargs={"pk": self.pk})



class XRayField(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    xray = models.FileField(verbose_name="xray_file", upload_to="XRay-data/", max_length=100)
    label = models.ForeignKey(
        FileLabel, verbose_name="xray_label", null=True, on_delete=models.SET_NULL
    )

    description = models.TextField(
        verbose_name="file_description", blank=True, null=True
    )
    uploaded_by = models.ForeignKey(
        CustomUser, related_name="uploaded_xrays", on_delete=models.CASCADE
    )
    uploaded_for = models.ForeignKey(
        CustomUser,
        related_name="xrays_for_review",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "XRayField"
        verbose_name_plural = "XRayFields"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("XRayField_detail", kwargs={"pk": self.pk})


"""
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    CONSULTATION DATA
//////////////////////////////////////////////
"""


class Consultation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    udpated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    Note = models.TextField(
        verbose_name="note",
        blank=True,
        null=True,
    )
    prescription_text = models.TextField(
        blank=True, null=True, verbose_name="prescription_text"
    )
    prescription = models.FileField(
        verbose_name="prescription",
        upload_to="prescription/",
        blank=True,
        null=True,
        max_length=100,
    )

    symptoms = models.ForeignKey(
        GeneralSymptom,
        blank=True,
        null=True,
        related_name="consultation",
        verbose_name="symptoms_data",
        on_delete=models.SET_NULL,
    )
    objects = ConsultationManager()
    class Meta:
        verbose_name = "Consultation"
        verbose_name_plural = "Consultations"

    def __str__(self):
        return "consultation_data"

    def get_absolute_url(self):
        return reverse("DoctorsConsultation_detail", kwargs={"pk": self.pk})
