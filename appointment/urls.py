from django.urls import path
from .views import TimeSlotView,AppointmentView

urlpatterns = [
    # request type get
    path("get-timeslots/", TimeSlotView.as_view()),
    path("get-timeslot/<int:pk>", TimeSlotView.as_view()),
    # request type post
    path("add-timeslot/", TimeSlotView.as_view()),
    # request type put
    path("update-timeslot/<int:pk>", TimeSlotView.as_view()),
    # request type delete
    path("delete-timeslot/<int:pk>", TimeSlotView.as_view()),
    # request type post
    path("book-appointment/",AppointmentView.as_view()),
    # request type get
    path("get-appointment/",AppointmentView.as_view()),
    # request type delete
    path("delete-appointment/<int:pk>",AppointmentView.as_view()),
]
