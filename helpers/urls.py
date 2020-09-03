from django.conf.urls import url,include
from . views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from rest_framework.authtoken import views
from .import views


urlpatterns = [

	url(r'^privacypolicy/$',TermAndConditionView.as_view()),
	url(r'^governmenthospitals/$',GovernmentHospitals.as_view()),
	url(r'^mixhospitals/$',MixHospitals.as_view()),

	url(r'^baramaticarecenters/$',BaramatiCareCenterHospitals.as_view()),
	url(r'^baramatiisolationcenters/$',BaramatiIsolationHospitals.as_view()),

	url(r'^districtcordinatorslist/$',DistrictCoordinatorContact.as_view()),
	
]