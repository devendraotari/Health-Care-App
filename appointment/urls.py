from django.urls import path
from .views import TimeSlotView,AppointmentView

urlpatterns = [
    # request type get
    path("get-timeslots/", TimeSlotView.as_view()),
    path("get-timeslot/<int:pk>", TimeSlotView.as_view()),
    # request type post
    path("add-timeslot/", TimeSlotView.as_view()),
    # request type put
    path("update-timeslot/", TimeSlotView.as_view()),
    # request type delete
    path("delete-timeslot/", TimeSlotView.as_view()),
    # request type post
    path("book-appointment/",AppointmentView.as_view()),
    # request type get
    path("get-appointment/",AppointmentView.as_view()),
    # request type delete
    path("delete-appointment/",AppointmentView.as_view()),
]
