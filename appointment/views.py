from django.http import request
from django.shortcuts import render
from django.db import transaction
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import RetrieveModelMixin

from covidUsers.models import CustomUser
from consultation.models import DoctorProfile, PatientProfile
from .models import Appointment, TimeSlot
from .serializers import AppointmentSerializer, TimeSlotSerializer
from consultation.api.utils import get_request_user
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


class TimeSlotView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, pk=None):
        user = get_request_user(request)
        content = None
        response_status = None
        if user:
            try:
                doctor_profile_id = request.data.get("doctor_profile_id", None)
                doc_profileObj = (
                    DoctorProfile.objects.all()
                    .select_related("doctor")
                    .filter(id=doctor_profile_id)
                )
                customUser_docObj = doc_profileObj.doctor
                if pk:
                    timeslots = TimeSlot.objects.all().filter(
                        Q(created_by=customUser_docObj) and Q(id=pk)
                    )
                else:
                    timeslots = TimeSlot.objects.all().filter(
                        created_by=customUser_docObj
                    )
                serialized = TimeSlotSerializer(timeslots, many=True)
                content = {"Appointment": serialized.data}
                response_status = status.HTTP_200_OK
            except ObjectDoesNotExist as odne:
                content = {
                    "Error": str(odne),
                    "msg": f"Timeslot with given Id {pk} doesn't exists",
                }
                response_status = status.HTTP_400_BAD_REQUEST

            except Exception as e:
                content = {"Error": str(e)}
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            content = {
                "msg": "Authentication token needed in request headers and user has to be a doctor"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(content, status=response_status)

    def post(self, request):
        user = get_request_user(request)
        content = None
        response_status = None
        if user and user.user_role.role == "D":
            created_by = user
            try:
                start_time_str = request.data.get("start_time", None)
                start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
                with transaction.atomic():
                    timeslot = TimeSlot(created_by=created_by, start_time=start_time)
                    timeslot.save()
                serialized = TimeSlotSerializer(timeslot)
                content = serialized.data
                response_status = status.HTTP_200_OK

            except ValueError as ve:
                content = {
                    "Error": f"{str(ve)}",
                    "message": "date string format should be 2020-10-03 18:34",
                }
                
            except Exception as e:
                content = {"error": f"{str(e)}"}
                response_status = status.HTTP_400_BAD_REQUEST

        else:
            content = {
                "msg": "Authentication token needed in request headers and user has to be a doctor"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(content, status=response_status)

    def delete(self, request, pk=None):
        user = get_request_user(request)
        content = None
        response_status = None
        if user and pk:
            created_by = user
            try:
                with transaction.atomic():
                    timeslot = (
                        TimeSlot.objects.all()
                        .filter(Q(created_by=created_by) and Q(id=pk))
                        .first()
                    )
                    timeslot.delete()
                content = {"msg": f"timeslot with id {pk} is deleted successfully"}
                response_status = status.HTTP_200_OK
            except Exception as e:
                content = {"error": f"{str(e)}"}
                response_status = status.HTTP_400_BAD_REQUEST

        else:
            content = {
                "msg": "Authentication token needed in request headers and user has to be a doctor"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(content, status=response_status)


class AppointmentView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, pk=None):
        user = get_request_user(request)
        content = None
        response_status = None
        if user and pk:
            appointment = Appointment.objects.get(id=pk)
            serialized = AppointmentSerializer(appointment)
            content = {"Appointments": serialized.data}
            response_status = status.HTTP_200_OK
        elif user:
            try:
                if user.user_role.role == "D":
                    doc_profileObj = DoctorProfile.objects.get(doctor=user)
                    appointments = Appointment.objects.all().filter(
                        Q(booking_slot__created_by=doc_profileObj)
                    )
                    serialized = AppointmentSerializer(appointments, many=True)
                    content = {"Appointments": serialized.data}
                    response_status = status.HTTP_200_OK

                if user.user_role.role == "P":
                    patient_profileObj = PatientProfile.objects.get(patient=user)
                    appointments = Appointment.objects.all().filter(
                        Q(booked_by=patient_profileObj)
                    )
                    serialized = AppointmentSerializer(appointments, many=True)
                    content = {"Appointments": serialized.data}
                    response_status = status.HTTP_200_OK

            except ObjectDoesNotExist as odne:
                content = {
                    "Error": str(odne),
                    "msg": f"Object does not exists",
                }
                response_status = status.HTTP_400_BAD_REQUEST

            except Exception as e:
                content = {"Error": str(e)}
                response_status = status.HTTP_400_BAD_REQUEST

        else:
            content = {
                "msg": "Authentication token needed in request headers and user has to be a doctor"
            }
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(content, status=response_status)

    def post(self, request):
        user = get_request_user(request)
        content = None
        response_status = None
        if user and user.user_role.role == "P":
            try:
                time_slot_id = request.data.get("time_slot_id", None)
                time_slotObj = TimeSlot.objects.get(id=time_slot_id)
                if time_slotObj.is_booked:
                    raise Exception("Timeslot is booked already")
                else:
                    time_slotObj.is_booked = True
                    time_slotObj.save()
                    appointment = Appointment(booked_by=user,booking_slot=time_slotObj)
                    appointment.save()
                    serialized = AppointmentSerializer(appointment)
                    content = serialized.data
                    response_status = status.HTTP_200_OK
            except Exception as e:
                content = {
                    "Error": f"{str(e)}",
                    "message": "select different timeslot",
                }
        else:
            content = {
                "msg": '''Authentication token needed in request 
                            headers and user has to be a doctor'''
            }
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(content, status=response_status)

    def delete(self,request,pk=None):
        user = get_request_user(request)
        content,response_status = (None,None)
        if user and pk:
            try:
                appointment = Appointment.objects.get(id=pk)
                time_slot = appointment.booking_slot
                time_slot.is_booked = False
                time_slot.save()
                appointment.delete()
                content = {"msg":f"Appointment with id {pk} is cancelled"}
            except ObjectDoesNotExist as odne:
                content = {"Error":f"{str(odne)}",
                            "msg":"Appointment for given id doesn't exist"
                }
        else:
            content = {
                "msg": '''Authentication token needed in request 
                            headers and user has to be a doctor'''
            }
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(content, status=response_status)