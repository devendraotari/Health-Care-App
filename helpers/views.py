from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.renderers import TemplateHTMLRenderer


class TermAndConditionView(APIView):
	permission_classes = []
	renderer_classes = [TemplateHTMLRenderer]

	def get(self, request):
		return Response(template_name='privacy_policy.html')
		

		# if self.request.query_params.get('lang'):
		# 	language = self.request.query_params.get('lang')
		# 	if language == 'en':
		# 		return Response(template_name='privacy_policy.html')
		# 	if language == 'mr':
		# 		return Response(template_name='marathiprivacy.html')
		# if not self.request.query_params.get('lang'):
		# 	return Response(status = 400)



class GovernmentHospitals(APIView):
	def get(self,request):
		
		try:
			if self.request.query_params.get('lang'):
				language = self.request.query_params.get('lang')
				if language == 'en':
					data_Obj = CoronaMaharastraGovermentHospital.objects.filter(lang = 'E')
				if language == 'mr':
					data_Obj = CoronaMaharastraGovermentHospital.objects.filter(lang = 'M')

				serializer = CoronaMaharastraGovermentHospitalSerializer(data_Obj, many = True)
				return Response(serializer.data , status = 200)
			else:
				return Response({"Error":"language is not defined"} , status=400)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class MixHospitals(APIView):
	def get(self,request):
		
		try:
			if self.request.query_params.get('lang'):
				language = self.request.query_params.get('lang')
				if language == 'en':
					data_Obj = MumbaiIsolationHospital.objects.filter(lang = 'E')
				if language == 'mr':
					data_Obj = MumbaiIsolationHospital.objects.filter(lang = 'M')

				serializer = MumbaiIsolationHospitalSerializer(data_Obj, many = True)
				return Response(serializer.data , status = 200)
			else:
				return Response({"Error":"language is not defined"} , status=400)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)


class BaramatiCareCenterHospitals(APIView):
	def get(self,request):
		
		try:
			if self.request.query_params.get('lang'):
				language = self.request.query_params.get('lang')
				if language == 'en':
					data_Obj = BaramatiCovidCareCenter.objects.filter(lang = 'E')
				if language == 'mr':
					data_Obj = BaramatiCovidCareCenter.objects.filter(lang = 'M')

				serializer = BaramatiCovidCareCenterSerializer(data_Obj, many = True)
				return Response(serializer.data , status = 200)
			else:
				return Response({"Error":"language is not defined"} , status=400)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class BaramatiIsolationHospitals(APIView):
	def get(self,request):
		
		try:
			if self.request.query_params.get('lang'):
				language = self.request.query_params.get('lang')
				if language == 'en':
					data_Obj = BaramatiIsolatuionCenter.objects.filter(lang = 'E')
				if language == 'mr':
					data_Obj = BaramatiIsolatuionCenter.objects.filter(lang = 'M')

				serializer = BaramatiIsolatuionCenterSerializer(data_Obj, many = True)
				return Response(serializer.data , status = 200)
			else:
				return Response({"Error":"language is not defined"} , status=400)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)


class DistrictCoordinatorContact(APIView):
	def get(self,request):
		
		try:
			if self.request.query_params.get('lang'):
				language = self.request.query_params.get('lang')
				if language == 'en':
					data_Obj = DistrictCordinator.objects.filter(lang = 'E')
				if language == 'mr':
					data_Obj = DistrictCordinator.objects.filter(lang = 'M')

				serializer = DistrictCordinatorSerializer(data_Obj, many = True)
				return Response(serializer.data , status = 200)
			else:
				return Response({"Error":"language is not defined"} , status=400)
		except Exception as e:
			return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)