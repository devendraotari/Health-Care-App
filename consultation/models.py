from django.db import models
from django.urls import reverse
from covidUsers.models import CustomUser

SPECIALITY_CHOICES = (
    ("cardiac", "Cardiologist"),
    ("ENT", "ENT specialist"),
    ("gastrologist", "stomach and digestion"),
    ("pediatrics", "pediatrics"),
    ("dermatology", "skin specialist"),
    ("dentist", "dentist"),
)

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


class Qualification(models.Model):
    degree = models.CharField(
        choices=QUALIFICATION_CHOICES, null=True, blank=True, max_length=50
    )
    institute = models.CharField(default="", null=True, blank=True, max_length=50)

    class Meta:
        verbose_name = "Qualification"
        verbose_name_plural = "Qualifications"

    def __str__(self):
        return f"{self.degree} from {self.institute}"

    def get_absolute_url(self):
        return reverse("Qualification_detail", kwargs={"pk": self.pk})


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
    # patient with whom doctor has consulted with
    patients = models.ManyToManyField(
        CustomUser,
        verbose_name="patients",
        related_name="patients",
    )
    speciality = models.CharField(
        choices=SPECIALITY_CHOICES, null=True, blank=True, max_length=50
    )
    experience = models.IntegerField(default=0, blank=True, null=True)
    description = models.TextField(default="", blank=True, null=True)
    qualification = models.ForeignKey(
        Qualification,
        verbose_name="qualification",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    fees = models.FloatField(blank=True, null=True, verbose_name="fees")

    class Meta:
        verbose_name = "DoctorProfile"
        verbose_name_plural = "DoctorProfiles"

    def __str__(self):
        return f"{self.doctor.name} speciality {self.speciality}"

    def get_absolute_url(self):
        return reverse("DoctorProfile_detail", kwargs={"pk": self.pk})


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

    class Meta:
        verbose_name = "PatientProfile"
        verbose_name_plural = "PatientProfiles"

    def __str__(self):
        return self.patient.name

    def get_absolute_url(self):
        return reverse("PatientProfile_detail", kwargs={"pk": self.pk})


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
    ecg_report = models.FileField(upload_to="ecg_reports/")
    temp = models.FloatField(blank=True, null=True, verbose_name="temperature")
    pulse = models.FloatField(blank=True, null=True, verbose_name="pulse")
    spo2 = models.FloatField(blank=True, null=True, verbose_name="oxygen_saturation")
    weight = models.FloatField(blank=True, null=True, verbose_name="weight")
    nutrition = models.TextField(default="", blank=True, null=True)
    nutrition_report = models.FileField(upload_to="nutrition_reports/")
    audiometry = models.FloatField(
        blank=True, null=True, verbose_name="autiometry_value"
    )
    audiometry_report = models.FileField(upload_to="audiometry_reports/")
    retina_scan = models.FloatField(blank=True, null=True, verbose_name="retina_scan")
    optometry = models.FloatField(blank=True, null=True, verbose_name="optometry")
    patient = models.ForeignKey(
        CustomUser,
        verbose_name="patient",
        related_name="from_patient",
        on_delete=models.PROTECT,
    )
    category = models.CharField(
        choices=SPECIALITY_CHOICES,
        blank=True,
        null=True,
        verbose_name="symptom_category",
        max_length=50,
    )
    assigned_doctor = models.ForeignKey(
        CustomUser,
        verbose_name="doctor",
        related_name="assigned_doctor",
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "GeneralSymptom"
        verbose_name_plural = "GeneralSymptoms"

    def __str__(self):
        return self.patient.name

    def get_absolute_url(self):
        return reverse("GeneralSymptom_detail", kwargs={"pk": self.pk})
