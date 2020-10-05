from django.db import models
from covidUsers.models import CustomUser
from datetime import datetime


class TimeSlot(models.Model):
    created_by = models.ForeignKey(
        CustomUser, related_name="available_slot", on_delete=models.CASCADE
    )
    start_time = models.DateTimeField(
        auto_now=False, auto_now_add=False, default=datetime.now()
    )
    is_booked = models.BooleanField(verbose_name="is_booked", default=False)

    def __str__(self):
        return "slot " + self.start_time


class Appointment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    booked_by = models.ForeignKey(
        CustomUser, related_name="appointment", on_delete=models.CASCADE
    )
    booking_slot = models.ForeignKey(
        TimeSlot, related_name="appointment", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=50, default="created")

    def __str__(self):
        return self.booked_by.__str__() + self.status
