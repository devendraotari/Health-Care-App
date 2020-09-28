from django.db import models
from consultation.models import PatientProfile, DoctorProfile
from covidUsers.models import CustomUser

# Create your models here.


class Order(models.Model):
    order_id = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    amount = models.IntegerField(verbose_name="total amount")
    amount_paid = models.IntegerField(verbose_name="amount paid")
    amount_due = models.IntegerField(verbose_name="amount due")
    currency = models.CharField(max_length=50)
    entity = models.CharField(max_length=50)
    attempts = models.IntegerField(verbose_name="attempts made", blank=True, null=True)
    receipt = models.CharField(max_length=50, blank=True, null=True)
    notes = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.IntegerField(verbose_name="created at")
    created_by = models.ForeignKey(
        PatientProfile,
        related_name="orders",
        verbose_name="created_by",
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    payment_for_doctor = models.ForeignKey(
        DoctorProfile, verbose_name="",
        related_name="orders", 
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.order_id

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})
