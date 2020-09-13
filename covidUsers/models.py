from django.db import models

# Create your models here.
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
# from .managers import UserManager
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.conf import settings
from .utils import *
from django.template.defaultfilters import slugify


GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    )


LANGUAGE_CHOICES = (
        ('E', 'English'),
        ('M', 'Marathi'),
    )

ROLE_CHOICES = (
        ('D', 'Doctor'),
        ('C', 'Counsellor'),
		('P','patient'),
        ('O', 'Others'),
    )
	
class Role(models.Model):
	role = models.CharField(choices=ROLE_CHOICES, max_length=50,unique=True, blank = True)

	def __str__(self):
		return self.role
	
class UserQuerySet(models.QuerySet):
	def all_doctors(self,*args, **kwargs):
		doctor_role = Role.objects.all().filter(role=ROLE_CHOICES[0][0]).first()
		return self.all().filter(user_role=doctor_role)

	def all_patients(self,*args, **kwargs):
		pass
	
	def all_patients_by_doctor(self,doctor=None,*args, **kwargs):
		pass

class UserManager(BaseUserManager):
	use_in_migrations = True

	def create_user(self,email,password,*args, **kwargs):
		user = self.model(email = self.normalize_email(email))
		user.username = email
		user.set_password(password)
		user.is_active = True
		print("printing kwargs")
		print(*args)
		print(kwargs)
		print("printing kwargs")
		user.user_role = kwargs['role']
		user.save()
		return user


	def create_superuser(self,username,email,password):
		user = self.create_user(email = email,password = password)
		user.is_staff = True
		user.is_superuser = True
		user.save()
		return user
	
	def get_queryset(self,*args, **kwargs):
		return UserQuerySet(self.model, using=self._db)
	
	def all_doctors(self,*args, **kwargs):
		return self.get_queryset().all_doctors()

	def all_patients(self,*args, **kwargs):
		return self.get_queryset().all_patients()

	def all_patients_by_doctor(self,doctor=None,*args, **kwargs):
		return self.get_queryset().all_patients_by_doctor(doctor,*args, **kwargs)

# changed name from dropdownValues to DropdownValues
class DropdownValues(models.Model):
	value = models.CharField(max_length=250 , blank = True , null = True)
	lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null = True, blank = True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	

	
	def __str__(self):
		return str(self.value)


class CustomUser(AbstractUser):
	name = models.CharField(max_length = 100, null = True, blank = True)
	email = models.EmailField(unique=False)
	phone = models.CharField(max_length = 100, null = True, blank = True)
	address = models.TextField(max_length = 100, blank = True)
	latitude = models.FloatField(default =0.0, blank = True)
	longitude = models.FloatField(default =0.0, blank = True)
	age = models.IntegerField(default=0.0)
	dob = models.DateField(blank=True,null=True)
	gender = models.CharField(max_length=2, choices=GENDER_CHOICES, null = True, blank = True) 
	otpVerified = models.BooleanField(default = False,null = True,blank =True)
	lang = models.ForeignKey(DropdownValues, on_delete = models.CASCADE,null = True,blank =True)
	user_role = models.ForeignKey(Role, verbose_name="user_role", related_name='user_role',null=True, on_delete=models.CASCADE) 
	createdAt = models.DateTimeField(auto_now_add = True)
	updatedAt = models.DateTimeField(auto_now = True)
	

	objects = UserManager()
	
	def __str__(self):
		return str(self.phone)

	class Meta:
		verbose_name_plural = "Users"

	REQUIRED_FIELDS = ['email']

	@receiver(post_save,sender = settings.AUTH_USER_MODEL)
	def create_auth_token(sender,instance = None, created = False,**kwargs):
		if created:
			Token.objects.create(user = instance)

	def covid_status(self):
		return 'Positive' if user_covid_status(user=self) else 'Negative'
	

class Choice(models.Model):
	choices= models.CharField(max_length=250)
	lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null = True, blank = True)
	isChecked = models.BooleanField(default = False)

	def __str__(self):
		return str(self.choices)



class CovidInitialQuestions(models.Model):
	question=models.TextField(null = True, blank = True)
	choices = models.ManyToManyField(Choice)
	lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null = True, blank = True)
	orderNumber = models.IntegerField(default=0 , null =True ,blank =True)
	isMultipleChoice = models.BooleanField(default = False)
	createdAt = models.DateTimeField(auto_now_add = True)
	updatedAt = models.DateTimeField(auto_now = True)


	def __str__(self):
		return str(self.question)


class CovidInitialQuestionsResponse(models.Model):
	question = models.ForeignKey(CovidInitialQuestions, on_delete = models.CASCADE,null = True,blank =True)
	user = models.ForeignKey(CustomUser,on_delete = models.CASCADE,null = True,blank =True)
	answer = models.ForeignKey(Choice ,on_delete = models.CASCADE,null = True,blank =True)
	createdAt = models.DateTimeField(auto_now_add = True)
	updatedAt = models.DateTimeField(auto_now = True)

	def __str__(self):
		return str(self.user)


class QuarantineSymptomsChoices(models.Model):
	choice = models.CharField(max_length=250)
	lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null = True, blank = True)
	isChecked = models.BooleanField(default = False)

	def __str__(self):
		return str(self.choice)

class QuarantineSymptomsQuestions(models.Model):
	symptom = models.TextField(null = True, blank = True)
	choices = models.ManyToManyField(QuarantineSymptomsChoices)
	lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null = True, blank = True)
	orderNumber = models.IntegerField(default=0 , null =True ,blank =True)
	finalAnswer = models.CharField(max_length = 100, null = True, blank = True, verbose_name ='finalAnswer')
	isMultipleChoice = models.BooleanField(default = False)
	createdAt = models.DateTimeField(auto_now_add = True)
	updatedAt = models.DateTimeField(auto_now = True)


	def __str__(self):
		return str(self.symptom)

class QurantineSymtomsAnswers(models.Model):
	question = models.ForeignKey(QuarantineSymptomsQuestions, on_delete = models.CASCADE,null = True,blank =True)
	answer = models.ForeignKey(QuarantineSymptomsChoices ,on_delete = models.CASCADE,null = True,blank =True)
	createdAt = models.DateTimeField(auto_now_add = True)
	updatedAt = models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.question.symptom + " : " + self.answer.choice + " \n"


class UserQuarantineSymptomsData(models.Model):
	user = models.ForeignKey('CustomUser',on_delete = models.CASCADE,null = True,blank =True)
	onDate = models.DateTimeField(blank=True,null=True)
	result = models.CharField(max_length = 100, null = True, blank = True, verbose_name ='result')	
	data = models.ManyToManyField(QurantineSymtomsAnswers, null=True,blank=True)

	def __str__(self):
		return str(self.user)



class CoronaHospital(models.Model):
	hospitalImage = models.ImageField(upload_to= "media/uploads/",null = True, blank = True ,verbose_name='Hospital Image')
	hospitalName = models.CharField(max_length = 255, null = True, blank = True , verbose_name ='Hospital Name')
	hospitalAddress = models.TextField(verbose_name ='Hospital Address')
	directions = models.CharField(max_length = 100, null = True, blank = True, verbose_name ='Directions')
	createdAt = models.DateTimeField(auto_now_add = True)
	updatedAt = models.DateTimeField(auto_now = True)

	def __str__(self):
		return str(self.hospitalName)
	
	class Meta:
		verbose_name_plural = "Corona Hospitals"


class NewsFeed(models.Model):
	image = models.ImageField(upload_to= "media/uploads/",null = True, blank = True ,verbose_name='Feed Image')
	video = models.FileField(upload_to= "media/uploads/",null = True, blank = True ,verbose_name='Feed Video')
	title = models.CharField(max_length = 255, null = True, blank = True,verbose_name ='Tilte')
	description = models.TextField(verbose_name ='Description',blank=True,null=True)
	link = models.CharField(max_length = 255, null = True, blank = True,verbose_name ='Link')
	lang = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null = True, blank = True)
	createdAt = models.DateTimeField(auto_now_add = True)
	updatedAt = models.DateTimeField(auto_now = True)

	# def __str__(self):
	# 	return self.hospitalName
	
	class Meta:
		verbose_name_plural = "News Feeds"


	@receiver(post_save,sender = 'covidUsers.NewsFeed')
	def send_push(sender,instance = None, created = False,**kwargs):
		if created:
			users = CustomUser.objects.all()
			for user in users:
				if UserFireBaseDeviceToken.objects.filter(user = user).exists():
					tokenObj = UserFireBaseDeviceToken.objects.get(user = user)
					message = "New Message"
					title = "COVID19-RAKSHAK"
					push_notification(tokenObj,message,title)
			instance.save()


class Message(models.Model):
	title = models.TextField(verbose_name ='Tilte',blank=True,null=True)
	question = models.TextField(verbose_name ='Message',blank=True,null=True)
	createdAt = models.DateTimeField(auto_now_add = True)
	updatedAt = models.DateTimeField(auto_now = True)

	# def __str__(self):
	# 	return self.hospitalName
	
	class Meta:
		verbose_name_plural = "Message Center"


	@receiver(post_save,sender = 'covidUsers.Message')
	def send_push(sender,instance = None, created = False,**kwargs):
		if created:
			users = CustomUser.objects.all()
			for user in users:
				if UserFireBaseDeviceToken.objects.filter(user = user).exists():
					tokenObj = UserFireBaseDeviceToken.objects.get(user = user)
					message = str(self.question)
					title = str(self.title)
					push_notification(tokenObj,message,title)
			instance.save()



class UserFireBaseDeviceToken(models.Model):
    user = models.ForeignKey('CustomUser', on_delete = models.CASCADE,null = True,blank =True)
    device_token = models.CharField(max_length = 255, default = "")
    device_type = models.CharField(max_length = 255, default = "")

    def __str__(self):
        return str(self.user)

class Links(models.Model):

	link = models.CharField(max_length = 255, null = True, blank = True, verbose_name ='Url')

	class Meta:
		verbose_name_plural = "Urls"

