from rest_framework import serializers
from .models import * 



class CustomUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
	email = serializers.SerializerMethodField()
	class Meta:
		model = CustomUser
		fields = (	'id',
					'name',
					# 'lastName',
					'email',
					# 'diabetic',
					# 'heartPatient',
					'dob',
					'age',
					'phone',
					'address',
					'latitude',
					'longitude',
					'gender',
					'otpVerified',
					'Volunteer',
					'createdAt',
					'updatedAt')

		depth = 1

	def get_email(self,obj):
		if obj.email == obj.phone:
			return ""
		else:
			return obj.email




class CoronaHospitalSerializer(serializers.ModelSerializer):
	class Meta:
		model = CoronaHospital
		fields = '__all__'



class NewsFeedSerializer(serializers.ModelSerializer):
	class Meta:
		model = NewsFeed
		fields = '__all__'


class QuarantineSymptomsQuestionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuarantineSymptomsQuestions
		fields = '__all__'
		depth = 2


class UserQuarantineSymptomsDataSerializer(serializers.ModelSerializer):
	# result = serializers.SerializerMethodField()
	class Meta:
		model = UserQuarantineSymptomsData
		fields = ('id','onDate','data')
		depth = 3

	# def get_result(self,obj):
	# 	print(obj)
	# 	count = 0
	# 	otherCount = 0
	# 	containmentCount = 0 
	# 	for data in obj.data.all():
	# 		if data.question == "Dry and Tight Cough" and data.answer == True:
	# 			count = count + 1

	# 		if data.question == "Difficulty Breathing" and data.answer == True:
	# 			count = count + 1

	# 		if data.question == "Shaking or Chills" and data.answer == True:
	# 			otherCount = otherCount + 1

	# 		if data.question == "Body Temperature" and data.answer != "98":
	# 			count = count + 1

	# 		if data.question == "Have you been to quarantined or visited any containment zone ?" and data.answer == True:
	# 			containmentCount = containmentCount + 1

	# 	if count >= 1 and otherCount == 1:
	# 		return "positive"

	# 	if  count >= 1 and otherCount == 1 and containmentCount == 1:
	# 		return "positive"

	# 	else:
	# 		return "negative"

		


class CovidInitialQuestionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = CovidInitialQuestions
		fields = ('id',
					'question',
					'choices',
					'isMultipleChoice',
					'orderNumber')

		depth = 2


class CovidInitialQuestionsResponseSerializer(serializers.ModelSerializer):
	class Meta:
		model = CovidInitialQuestionsResponse
		fields = ('id','question','answer')
		depth = 1


class dropdownSerializer(serializers.ModelSerializer):
	class Meta:
		model = dropdownValues
		fields = ('id','value')
		