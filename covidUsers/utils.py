import requests
import json
from rest_framework import status
import traceback
from .models import *


 

def push_notification(user_firebase_obj, message_body, message_title):
	try:
		# firebase_obj  = FirebaseCredentials.objects.get(slug = 'firebase')
		server_key = "AAAAKkoCM0M:APA91bGSky62iabR6xlhFx9qiduTewU81RMKxvDtbb-56TtymTNDG4eLdVZkE07CY1a4Q1ql0e3UG-BsETLTfhjEhRBe2aGVYqUqoXdcV8mZp3dTCMDVY1bM463lD5QlZwz8sseWkyHi"

		url = "https://fcm.googleapis.com/fcm/send"
		headers = {
		    'authorization': "key="+str(server_key),
		    'content-type': "application/json",
		    }
		payload_android = {
		 "content_available": True,
				  "notification": {
					  "title": message_title,
					  "sound":"default",
					  "body": message_body,
					  "badge": 6, 
					  "notification-type":"chat"
				 	},
				  "to": user_firebase_obj.device_token,
				  "priority": "high"
		}

		payload_ios = {
		 "content_available": True,
				  "notification": {
					  "title": message_title,
					  "sound":"default",
					  "body": message_body,
					  "badge": 6, 
					  "notification-type":"chat"
				 	},
				  "to": user_firebase_obj.device_token,
				  "priority": "high"
		}
		if user_firebase_obj.device_type == "Android":
			payload = json.dumps(payload_android)
			print ("ANDROID")
		else:
			payload = json.dumps(payload_ios)
			print ("IOS")


		response = requests.request("POST", url, data=payload, headers = headers)
		print (response)

	except Exception as e:
		traceback.print_exc()
		return str(e)


	

from datetime import date

def calculate_age(born):
	today = date.today()
	return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def user_covid_status(user):
	from .models import CovidInitialQuestionsResponse
	highRisk = []
	highRiskCount = 0
	mediumRisk = []
	mediumRiskCount = 0
	covidpositive = False
	if user.dob:
		age = calculate_age(user.dob)
	else:
		age = user.age
	data_Obj = CovidInitialQuestionsResponse.objects.filter(user = user)

	language = 'E'
	if data_Obj:

		for obj in data_Obj:
			question = obj.question
			ans = obj.answer
			language = ans.lang

			if question.question == 'Yes - Positive' and ans.choices == 'True':
				covidpositive = True
				break

			if question.question == 'होय- सकारात्मक' and ans.choices == 'होय':
				covidpositive = True
				break

			if question.question == 'Do you currently have any of the following symptoms?\r\nSelect all that apply :' and ans.choices == 'Fever':
				highRisk.append('Fever')
				mediumRisk.append('Fever')

			if question.question == 'आपणामध्ये खालीलपैकी कोणतेही एक लक्षण आहे काय? (जे सर्व लागू असतील ते निवडा ):' and ans.choices == 'ताप':
				highRisk.append('ताप')
				mediumRisk.append('ताप')

			if question.question == 'Do you currently have any of the following symptoms?\r\nSelect all that apply :' and  ans.choices == 'Coughing':
				highRisk.append('Coughing')
				mediumRisk.append('Coughing')

			if question.question == 'आपणामध्ये खालीलपैकी कोणतेही एक लक्षण आहे काय? (जे सर्व लागू असतील ते निवडा ):' and ans.choices == 'खोकला':
				highRisk.append('खोकला')
				mediumRisk.append('खोकला')

			# if question.question == 'Are you 60 years old or older?' and ans.choices == 'True':
			if age <= 60:
				mediumRiskCount = mediumRiskCount + 1
			

			if age > 60:
				highRiskCount = highRiskCount + 1

			if question.question == 'आपण ६० वर्षे किंवा त्यापेक्षा जास्त वयाचे आहात ?' and ans.choices == 'होय':
				highRiskCount = highRiskCount + 1

			
			# if question.question == 'Are you 60 years old or older?' and ans.choices == 'False':
			# 	mediumRiskCount = mediumRiskCount + 1

			if question.question == 'आपण ६० वर्षे किंवा त्यापेक्षा जास्त वयाचे आहात ?' and ans.choices == 'नाही':
				mediumRiskCount = mediumRiskCount + 1
			
			if question.question == 'In the past 14 days, have you had contact (of more than 15 Mins at less than 6 feet distance) with someone whose laboratory diagnosis of COVID -19 is confirmed?' and ans.choices == 'True':
				highRiskCount = highRiskCount + 1
			else:
				mediumRiskCount = mediumRiskCount + 1

			if question.question == 'मागील  १४ दिवसामध्ये आपला अशा व्यक्तीशी संपर्क आला आहे का ज्याचा  कोविड १९ साठीचा   प्रयोगशाळा अहवाल सकारात्मक आला आहे ? ( सहा फूट अंतराच्या  १५ मिनिटांकरिता )' and ans.choices == 'होय':
				highRiskCount = highRiskCount + 1
			else:
				mediumRiskCount = mediumRiskCount + 1

			if question.question == 'Within the past 14 days. Have you traveled (Internationally or Domestically)?' and ans.choices == 'International':
				highRiskCount = highRiskCount + 1
			else:
				mediumRiskCount = mediumRiskCount + 1

			if question.question == 'मागील  १४ दिवसामध्ये आपण  आंतर राष्ट्रीय अथवा राष्ट्रीय  स्तरावर प्रवास केला आहे का ?' and ans.choices == 'आंतर राष्ट्रीय':
				highRiskCount = highRiskCount + 1
			else:
				mediumRiskCount = mediumRiskCount + 1

			if question.question == 'Please select any chronic conditions that you are currently managing. Select all that apply :' and ans.choices == 'Chronic lung disease(COPD, Asthma etc.)':
				highRiskCount = highRiskCount + 1
			else:
				mediumRiskCount = mediumRiskCount + 1

			if question.question == 'आपणास  खालीलपैकी कोणत्याही  दीर्घकालीन  आजारावर औषोधोपचार सुरु  आहेत काय? असल्यास  ते निवडा  :' and ans.choices == 'दीर्घकालीन फुफ्फुसाचा आजार':
				highRiskCount = highRiskCount + 1
			else:
				mediumRiskCount = mediumRiskCount + 1
		if not covidpositive:
			if language:
				if language == 'E':
					high =  any(elem in ['Fever','Coughing'] for elem in highRisk )	
					
					if high == True and highRiskCount >= 1:
						covidpositive = True
					

					elif high == False and highRiskCount >= 1:
						covidpositive = True
					
					medium = any(elem in ['Fever','Coughing']  for elem in mediumRisk)	

					if medium == True and mediumRiskCount >= 3:
						covidpositive = True

					if medium == False and mediumRiskCount >= 3:
						covidpositive = False

				if language == 'M':
					high =  any(elem in ['ताप','खोकला'] for elem in highRisk )	
					
					if high == True and highRiskCount >= 1:
						covidpositive = True
					

					elif high == False and highRiskCount >= 1:
						covidpositive = True

					
					medium = any(elem in ['ताप','खोकला']  for elem in mediumRisk)	

					if medium == True and mediumRiskCount >= 3:
						covidpositive = True
					
					if medium == False and mediumRiskCount >= 3:
						covidpositive = False
	
	return covidpositive


def get_postive(user=None, forPositive=True):
	from .models import CustomUser
	if not user:
		userObjs = CustomUser.objects.filter(is_superuser=False)
		positiveusers = []
		for user in userObjs:
			
			covidpositive = user_covid_status(user) 
			if covidpositive:
				positiveusers.append(user.id)

		if forPositive:
			return CustomUser.objects.filter(id__in=positiveusers)
		else:
			return CustomUser.objects.filter(is_superuser=False).exclude(id__in=positiveusers)
	else:
		covidpositive = user_covid_status(user) 
		if covidpositive:
			positiveusers.append(user.id)