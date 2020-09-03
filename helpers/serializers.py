from rest_framework import serializers
from .models import * 



class CoronaMaharastraGovermentHospitalSerializer(serializers.ModelSerializer):
	class Meta:
		model = CoronaMaharastraGovermentHospital
		fields = '__all__'




class MumbaiIsolationHospitalSerializer(serializers.ModelSerializer):
	class Meta:
		model = MumbaiIsolationHospital
		fields = '__all__'




class BaramatiCovidCareCenterSerializer(serializers.ModelSerializer):
	class Meta:
		model = BaramatiCovidCareCenter
		fields = '__all__'




class BaramatiIsolatuionCenterSerializer(serializers.ModelSerializer):
	class Meta:
		model = BaramatiIsolatuionCenter
		fields = '__all__'




class DistrictCordinatorSerializer(serializers.ModelSerializer):
	class Meta:
		model = DistrictCordinator
		fields = '__all__'
		depth = 1

