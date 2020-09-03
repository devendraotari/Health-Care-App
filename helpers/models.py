from django.db import models

# Create your models here.
TYPE_CHOICES = (
        ('govt', 'Goverment'),
        ('pvt', 'Private'),
        ('mcg', 'MCGM'),
    )

LANGUAGE_CHOICES = (
        ('E', 'English'),
        ('M', 'Marathi'),
    )


class CoronaMaharastraGovermentHospital(models.Model):
	district =  models.CharField(max_length = 255, null = True, blank = True , verbose_name ='District')
	hospitalName = models.CharField(max_length = 255, null = True, blank = True , verbose_name ='Hospital Name')
	numberOfBeds = models.CharField(max_length = 255, null = True, blank = True , verbose_name ='No of Beds')
	lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null = True, blank = True)
	directions = models.CharField(max_length = 255, null = True, blank = True , verbose_name ='Directions')
	createdAt = models.DateTimeField(auto_now_add = True)
	updatedAt = models.DateTimeField(auto_now = True)

	def __str__(self):
		return str(self.hospitalName)
	
	class Meta:
		verbose_name_plural = "Maharastra Goverment Hospitals" 


class MumbaiIsolationHospital(models.Model):
	ward =  models.CharField(max_length = 255, null = True, blank = True , verbose_name ='Ward')
	area =  models.CharField(max_length = 255, null = True, blank = True , verbose_name ='Area')
	hospitalName = models.CharField(max_length = 255, null = True, blank = True , verbose_name ='Hospital Name')
	numberOfBeds = models.CharField(max_length = 255, null = True, blank = True , verbose_name ='No of Beds')
	hospitalType = models.CharField(max_length=100, choices=TYPE_CHOICES, null = True, blank = True)
	lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null = True, blank = True)
	directions = models.CharField(max_length = 255, null = True, blank = True , verbose_name ='Directions')
	createdAt = models.DateTimeField(auto_now_add = True)
	updatedAt = models.DateTimeField(auto_now = True)

	def __str__(self):
		return str(self.hospitalName)
	
	class Meta:
		verbose_name_plural = "Mumbai Isolation Hospitals" 



class BaramatiCovidCareCenter(models.Model):
	district = models.CharField(max_length = 255, null = True, blank = True,verbose_name ='District')
	centerName = models.CharField(max_length = 255, null = True, blank = True,verbose_name ='Covid Care Center Name')
	centerAddress = models.CharField(max_length = 255, null = True, blank = True,verbose_name ='Covid Care Center Address')
	availableBeds = models.CharField(max_length = 100, null = True, blank = True,verbose_name ='Available Beds')
	ambulanceNumber = models.CharField(max_length = 100, null = True, blank = True,verbose_name ='Ambulance Number')
	contactPerson = models.CharField(max_length = 100, null = True, blank = True,verbose_name ='Contact Person Name')
	phone = models.CharField(max_length = 100, null = True, blank = True,verbose_name ='Contact Person Ph. Number')
	assignedDhch = models.CharField(max_length = 100, null = True, blank = True,verbose_name ='Assigned DHCH')
	lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null = True, blank = True)


	def __str__(self):
		return str(self.centerName)

	class Meta:
		verbose_name_plural = "Baramati Covid Care Centers" 


class BaramatiIsolatuionCenter(models.Model):
	name = models.CharField(max_length = 255, null = True, blank = True,verbose_name ='Hospital Name')
	totalBed = models.CharField(max_length = 255, null = True, blank = True,verbose_name ='Total Beds')
	isolationBed = models.CharField(max_length = 255, null = True, blank = True,verbose_name ='Isolation Beds')
	remark = models.CharField(max_length = 100, null = True, blank = True,verbose_name ='Remarks')
	lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null = True, blank = True)
	


	def __str__(self):
		return str(self.name)

	class Meta:
		verbose_name_plural = "Baramati Isolation Centers" 



class DistrictChairman(models.Model):
	chairmanName = models.CharField(max_length = 255, null = True, blank = True,verbose_name ='Chairman Name')
	phone = models.CharField(max_length = 255, null = True, blank = True,verbose_name ='Primary Phone No.')
	secondPhone = models.CharField(max_length = 255, null = True, blank = True,verbose_name ='Secondary Phone No.')
	lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null = True, blank = True)

	def __str__(self):
		return str(self.chairmanName)




class DistrictCordinator(models.Model):
	district = models.CharField(max_length = 255, null = True, blank = True,verbose_name ='District')
	distCommiteChairman = models.ManyToManyField(DistrictChairman, verbose_name = 'District Committee Chairman')
	lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null = True, blank = True)


	def __str__(self):
		return str(self.district)
