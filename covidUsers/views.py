from django.shortcuts import render

# Create your views here.
from .serializers import * 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import DatabaseError, transaction
import traceback
from .models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import traceback
from .utils import * 



# from rest_framework.generics import GenericAPIView


class RoleView(APIView):
	def get(self,request):
		data = Role.objects.all()
		try:
			serialized = RoleSerializer(data,many=True)
			return Response(serialized.data,status=status.HTTP_200_OK)
		except Exception as e:
			traceback.print_exc()
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class UserProfile(APIView):
	permission_classes = ()
	
	def post(self, request):
		data = request.data
		role = None

		if CustomUser.objects.filter(phone = data.get('phone')).exists():
			return Response({'Error': "user with this phone already exists"}, status = status.HTTP_400_BAD_REQUEST)
		if data.get('role')=='P':
			role = Role.objects.all().filter(role='P').first()
			# print(f"role instance type -> {type(patient_role_instance)}")
			# user.user_role = patient_role_instance
		if data.get('role')=='D':
			role = Role.objects.all().filter(role='D').first()
			# print(f"role instance type -> {type(doctor_role_instance)}")
			# user.user_role = doctor_role_instance
		try:
			with transaction.atomic():
				user = CustomUser.objects.create_user(
					email = data.get('email', None) if data.get('email') else data.get('phone') ,
					password = data.get('phone', None),role = role)
				
				user.name = data.get('name', None)
				user.gender = data.get('gender', None)
				user.dob = data.get('dob', None)
				user.age = data.get('age', 0)
				user.phone = data.get('phone', None)
				user.address = data.get('address', None)
				user.otpVerified = data.get('otpVerified', None)
				user.latitude = data.get('latitude', None)
				user.longitude = data.get('longitude', None)
				print('********before save transcaction atomic *******')
				user.save()
				print('******** after save transcaction atomic *******')
				
				if 'device_token' in data and 'device_type' in data:		
					obj, created = UserFireBaseDeviceToken.objects.update_or_create(
								user = user,
								device_token = data.get('device_token'),
								device_type = data.get('device_type')
								)		
					# saveuser_deviceid(user, , )

				serialized = CustomUserSerializer(user)
				
				token_obj = Token.objects.get(user = user)
				response = {'key': token_obj.key}

				return Response(response, status = status.HTTP_201_CREATED)
		except Exception as e:
			traceback.print_exc()
			return Response({'Error': "Unable to create user, try agian"}, status = status.HTTP_400_BAD_REQUEST)


class loginAPIView(APIView):
	permission_classes = ()
	
	def post(self,request):
		data = request.data
		print (data)
		if CustomUser.objects.filter(phone = data.get('phone')).exists():
			user = CustomUser.objects.get(phone = data.get('phone'))
			token_obj = Token.objects.get(user = user)
			response = {'key': token_obj.key}
			return Response(response, status = 200)
		else:
			return Response({'detail': "Phone number not exists."}, status = status.HTTP_202_ACCEPTED)

class Me(APIView):

	def get(self,request):
		user = request.user
		try:
			serialized = UserProfileSerializer(user)
			return Response(serialized.data,status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class HospitalDetails(APIView):
	
	def get(self,request):
		data = CoronaHospital.objects.all()
		try:
			serialized = CoronaHospitalSerializer(data , many = True , context = {'request': request})
			return Response(serialized.data,status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class NewsFeedDetails(APIView):
	
	def get(self,request):
		try:
			if self.request.query_params.get('lang'):
				language = self.request.query_params.get('lang')
				if language == 'en':
					data_Obj = NewsFeed.objects.filter(lang = 'E')
				if language == 'mr':
					data_Obj = NewsFeed.objects.filter(lang = 'M')

				serializer = NewsFeedSerializer(data_Obj , many = True , context = {'request': request})
				return Response(serializer.data , status = 200)
			else:
				return Response({"Error":"language is not defined"} , status=400)


			# serialized = NewsFeedSerializer(data , many = True , context = {'request': request})
			# return Response(serialized.data,status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)



class UserQuarantineSymptoms(APIView):
	def get(self,request):
		
		try:
			if self.request.query_params.get('lang'):
				language = self.request.query_params.get('lang')
				if language == 'en':
					data_Obj = QuarantineSymptomsQuestions.objects.filter(lang = 'E')
				if language == 'mr':
					data_Obj = QuarantineSymptomsQuestions.objects.filter(lang = 'M')

				serializer = QuarantineSymptomsQuestionsSerializer(data_Obj, many = True)
				return Response(serializer.data , status = 200)
			else:
				return Response({"Error":"language is not defined"} , status=400)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)


class DailyData(APIView):

	def post(self,request):
		data = request.data
		user = request.user
		count = 0
		otherCount = 0
		containmentCount = 0 
		coughFrequencyCount = 0
		CovidPostive = False
		try:

			if UserQuarantineSymptomsData.objects.filter(Q(onDate= data.get('onDate')) & Q(user = user)).exists():
					return Response({"Error": "data already exists"}, status = 400)

			dataObj = UserQuarantineSymptomsData.objects.create(
					user = user,
					onDate = data.get('onDate')
				)
			for objId in data.get('data'):
				
				questionObj = QuarantineSymptomsQuestions.objects.get(id = objId.get('symptom'))
				answerObj = QuarantineSymptomsChoices.objects.get(id = objId.get('answer'))
				print (questionObj.symptom)
				print (answerObj.choice)

			
				ansObj = QurantineSymtomsAnswers.objects.create(
					question = questionObj,
					answer = answerObj
					)
				dataObj.data.add(ansObj)
				dataObj.save()

				if questionObj.symptom == "Was the Covid test positive ?" and answerObj.choice == 'True':
					# count = count + 1
					# return Response({"result":"positive"} , status = 200)
					CovidPostive = True
				# #############################  OTHERS  ############################# 
				if questionObj.symptom == "Dry and Tight Cough" and answerObj.choice == 'True':
					otherCount = otherCount + 1

				if questionObj.symptom == "Difficulty Breathing" and answerObj.choice == 'True':
					otherCount = otherCount + 1

				if questionObj.symptom == "Shaking or Chills" and answerObj.choice == 'True':
					otherCount = otherCount + 1
				# #############################  OTHERS  #############################


				# #############################  Body Temperature  #############################
				if questionObj.symptom == "Body Temperature" and answerObj.choice in ["102-104", "104+", "High Fever", "Very High Fever"]:
					count = count + 1
				# #############################  Body Temperature  #############################

				if questionObj.symptom == "Have you been to quarantined or visited any containment zone ?" and answerObj.choice == 'True':
					containmentCount = containmentCount + 1

				# #############################  COUGH FREQUENCY  ############################# 
				if questionObj.symptom == "Cough Frequency" and answerObj.choice in ["Very Frequent", "Severe"]:
					coughFrequencyCount = coughFrequencyCount + 1
				# #############################  COUGH FREQUENCY  ############################# 



				# #############################  COUGH FREQUENCY  ############################# 
				if questionObj.symptom == "खोकला वारंवारता" and answerObj.choice in ["खूपच वारंवार", "गंभीर"]:
					coughFrequencyCount = coughFrequencyCount + 1
				# #############################  COUGH FREQUENCY  ############################# 

				if questionObj.symptom == "कोविड चाचणी सकारात्मक होती का?" and answerObj.choice == 'होय':
					# count = count + 1
					CovidPostive = True
					# return Response({"result":"positive"} , status = 200)
				
				# #############################  OTHERS  ############################# 
				if questionObj.symptom == "कोरडा खोकला" and answerObj.choice == 'होय':
					otherCount = otherCount + 1

				if questionObj.symptom == "श्वास घेण्यास त्रास" and answerObj.choice == 'होय':
					otherCount = otherCount + 1

				if questionObj.symptom == "थरथरणे किंवा थंडी वाजून येणे" and answerObj.choice == 'होय':
					otherCount = otherCount + 1
				# #############################  OTHERS  ############################# 

				# #############################  Body Temperature  #############################
				if questionObj.symptom == "शरीराचे तापमान" and answerObj.choice in ["102-104", "104+", "उच्च ताप" , "खूप उच्च ताप"]:
					count = count + 1
				# #############################  Body Temperature  #############################

				if questionObj.symptom == "आपण कोणत्याही कंटेन्ट झोनला अलग ठेवण्यास किंवा भेट दिली आहे?" and answerObj.choice == 'होय':
					containmentCount = containmentCount + 1

			if CovidPostive:
				return Response({"result":"positive"} , status = 200)

			if containmentCount != 0 and count !=0 and coughFrequencyCount !=0:
				return Response({"result":"positive"} , status = 200)

			if containmentCount != 0 and count !=0 and otherCount !=0:
				return Response({"result":"positive"} , status = 200)

			if count !=0 and coughFrequencyCount !=0 and otherCount !=0:
				return Response({"result":"positive"} , status = 200)

			if count !=0 and otherCount == 3:
				return Response({"result":"positive"} , status = 200)

			return Response({"result":"negative"} , status = 200)
			# if count >= 1 and otherCount >= 0:
			# 	serializer = UserQuarantineSymptomsDataSerializer(dataObj,many =True)
			# 	return Response({"result":"positive"} , status = 200)

			# if  count >= 1 and otherCount >= 0 and containmentCount == 1:
			# 	serializer = UserQuarantineSymptomsDataSerializer(dataObj,many =True)
			# 	return Response({"result":"positive"} , status = 200)

			# else:
			# 	serializer = UserQuarantineSymptomsDataSerializer(dataObj,many =True)
			# 	return Response({"result":"negative"} , status = 200)


				
			# serializer = UserQuarantineSymptomsDataSerializer(dataObj,many =True)
			# return Response({"result":"Response saved"} , status = 200)
		except Exception as e:
			traceback.print_exc()
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)
		
	
	def get(self,request):
		user = request.user
		try:
			data_Obj = UserQuarantineSymptomsData.objects.filter(user = user).order_by('id')
			serializer = UserQuarantineSymptomsDataSerializer(data_Obj, many = True)
			return Response(serializer.data , status = 200)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)




class UserIntialQuestionsAnswers(APIView):

	def post(self,request):
		data = request.data
		user = request.user
		print (data)
		try:
			for objId in data:
				questionObj = CovidInitialQuestions.objects.get(id = objId.get('question'))
				answerObj = Choice.objects.get(id = objId.get('answer'))

				if CovidInitialQuestionsResponse.objects.filter(Q(user = user) & Q(question = questionObj) & Q(answer = answerObj)).exists():
					return Response({"Error": "data already exists"}, status = 400)
				
				dataObj = CovidInitialQuestionsResponse.objects.create(
					user = user,
					question = questionObj,
					answer = answerObj
				)
			serializer = CovidInitialQuestionsResponseSerializer(dataObj)
			return Response({"success":"Response saved"} , status = 200)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)
		
	def get(self,request):
		user = request.user
		highRisk = []
		highRiskCount = 0
		mediumRisk = []
		mediumRiskCount = 0

		
		try:
			if user.dob:
				age = calculate_age(user.dob)
			else:
				age = user.age
			data_Obj = CovidInitialQuestionsResponse.objects.filter(user = user)

			if data_Obj:
		
				for obj in data_Obj:
					question = CovidInitialQuestions.objects.get(id = obj.question.id)
					ans = Choice.objects.get(id =obj.answer.id)

					if question.question == 'Yes - Positive' and ans.choices == 'True':
						return Response({"risk":"High"} , status = 200)

					if question.question == 'होय- सकारात्मक' and ans.choices == 'होय':
						return Response({"risk":"High"} , status = 200)

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
				
				if self.request.query_params.get('lang'):
					language = self.request.query_params.get('lang')
					if language == 'en':
						print ("EN")
						high =  any(elem in ['Fever','Coughing'] for elem in highRisk )	
						
						if high == True and highRiskCount >= 1:
							return Response({"risk":"High"} , status = 200) 
						

						elif high == False and highRiskCount >= 1:
							return Response({"risk":"Medium"} , status = 200) 

						
						medium = any(elem in ['Fever','Coughing']  for elem in mediumRisk)	

						if medium == True and mediumRiskCount >= 3:
							return Response({"risk":"Medium"} , status = 200) 
						
						if medium == False and mediumRiskCount >= 3:
							return Response({"risk":"Low"} , status = 200)
					
					if language == 'mr':
						print ("MR")
						high =  any(elem in ['ताप','खोकला'] for elem in highRisk )	
						
						if high == True and highRiskCount >= 1:
							return Response({"risk":"High"} , status = 200) 
						

						elif high == False and highRiskCount >= 1:
							return Response({"risk":"Medium"} , status = 200) 

						
						medium = any(elem in ['ताप','खोकला']  for elem in mediumRisk)	

						if medium == True and mediumRiskCount >= 3:
							return Response({"risk":"Medium"} , status = 200) 
						
						if medium == False and mediumRiskCount >= 3:
							return Response({"risk":"Low"} , status = 200)
			else:
				return Response({"error":"Data not exists"} , status = 400)		
			# serializer = CovidInitialQuestionsResponseSerializer(data_Obj, many = True)
			# return Response(serializer.data , status = 200)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)


class UserQuestions(APIView):
	permission_classes =()
	def get(self,request):
		user = request.user
		
		try:
			
			if self.request.query_params.get('lang'):
				language = self.request.query_params.get('lang')
				if language == 'en':
					if (user.gender == "M") or (user.gender == "O"):
						data_Obj = CovidInitialQuestions.objects.filter(lang = 'E').exclude(orderNumber = 7)
					else:
						data_Obj = CovidInitialQuestions.objects.filter(lang = 'E')
				if language == 'mr':
					if (user.gender == "M") or (user.gender == "O"):
						data_Obj = CovidInitialQuestions.objects.filter(lang = 'M').exclude(orderNumber = 7)
					else:
						data_Obj = CovidInitialQuestions.objects.filter(lang = 'M')

				serializer = CovidInitialQuestionsSerializer(data_Obj, many = True)
				return Response(serializer.data , status = 200)
			else:
				return Response({"Error":"language is not defined"} , status=400)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)



		
class UpdateFirebaseDetail(APIView):

	def put(self, request):
		data = request.data
		loggedin_user = request.user
		try:
			if ('device_token' not in data) and ('device_type' not in data):
				return Response({'error': "Please provide device_token and device_type "}, status = status.HTTP_400_BAD_REQUEST)

			if UserFireBaseDeviceToken.objects.filter(user = request.user).exists():
				firebase_obj = UserFireBaseDeviceToken.objects.get(user = request.user)
				firebase_obj.device_token = data.get('device_token')
				firebase_obj.device_type=data.get('device_type')
				firebase_obj.save()
				# print(firebase_obj.firebase_token,firebase_obj.device_type)
				return Response({'success': True}, status = status.HTTP_200_OK)
			else:
				UserFireBaseDeviceToken.objects.create(
				user  = loggedin_user,
				device_token = data.get('device_token'),
				device_type = data.get('device_type'))

				return Response({'success': True}, status = status.HTTP_200_OK)
		except Exception as e:
			traceback.print_exc(e)
			return Response(str(e), status = status.HTTP_400_BAD_REQUEST)

class DeletUser(APIView):
	permission_classes = []
	def post(self,request):
		try:
			if CustomUser.objects.filter(phone = data.get('phone')).exists():
				obj = CustomUser.objects.get(phone = data.get('phone'))
				obj.delete()
				return Response({"success":"user deleted"} , status=400)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)


class DropdownValuesAPI(APIView):
	permission_classes = []

	def get(self,request):
		try:
			if self.request.query_params.get('lang'):
				language = self.request.query_params.get('lang')
				if language == 'en':
					data_Obj = dropdownValues.objects.filter(lang = 'E')
				if language == 'mr':
					data_Obj = dropdownValues.objects.filter(lang = 'M')
			
			serialized = dropdownSerializer(data_Obj , many =True)
			return Response(serialized.data,status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class ReturnUrl(APIView):
	permission_classes = []

	def get(self, request):
		try:
			linkObj = Links.objects.all()[0]
		except:
			linkObj = None

		return Response({
			"url" : linkObj.link if linkObj else ""
			})