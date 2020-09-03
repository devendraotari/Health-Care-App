from django.conf.urls import include, url
from django.contrib import admin
from .views import *
from . import views


urlpatterns = [
	# url(r'^auth/', include('rest_auth.urls')),
	url(r'^login/$', loginAPIView.as_view()),
	url(r'^me/$', Me.as_view()),
	url(r'^createuser/$', UserProfile.as_view()),
	
	url(r'^hospitalslist/$', HospitalDetails.as_view()),
	url(r'^newsfeedlist/$', NewsFeedDetails.as_view()),
	
	url(r'^userquarantineymptoms/$', UserQuarantineSymptoms.as_view()),
	url(r'^userdailydata/$', DailyData.as_view()),
	
	url(r'^userinitialquestions/$', UserIntialQuestionsAnswers.as_view()),
	url(r'^userquestions/$', UserQuestions.as_view()),
	
	url(r'^updatefirebasedetail/$', UpdateFirebaseDetail.as_view()),
	url(r'^deleteuser/$', DeletUser.as_view()),

	url(r'^dropdownvalues/$', DropdownValuesAPI.as_view()),

	url(r'^link/$', ReturnUrl.as_view()),

	
	
]
