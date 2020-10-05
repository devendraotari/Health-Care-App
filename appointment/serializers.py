from django.db.models import fields
from rest_framework import serializers

from .models import TimeSlot,Appointment
from covidUsers.serializers import CustomUserSerializer

class TimeSlotSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer()
    class Meta:
        model = TimeSlot
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    booked_by = CustomUserSerializer()
    booking_slot = TimeSlotSerializer()

    class Meta:
        model = Appointment
        fields = '__all__'