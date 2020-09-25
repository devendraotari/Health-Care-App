from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from import_export.admin import ExportActionMixin, ExportMixin
from import_export import resources, formats as FORMATS
from import_export.fields import Field
from .utils import get_postive

# admin.site.unregister(Group)

# from import_export.widgets import JSONWidget, ManyToManyWidget, ForeignKeyWidget
# import json


# class MultiSymptomValues(ManyToManyWidget):

# 	def render(self, value, obj=None):
# 		print(value)
# 		return json.dumps(
# 			list(value.values('data__question', 'data__answer'))
# 			)

class CovidPositiveFilter(admin.SimpleListFilter):
	title = 'Covid Status'
	parameter_name = 'Covid'

	def lookups(self, request, model_admin):
		return [('postive', 'Postive'), ('negative', 'Negative')]

	def queryset(self, request, queryset):
		if self.value() == 'postive':
			return get_postive()
			# return queryset.filter(id=0)
		elif self.value() == 'negative':
			return get_postive(forPositive=False)
		else:
			queryset

class CustomUserResource(resources.ModelResource):
	# symptoms = Field()
	# answers = Field()
	covid_status = Field()
	class Meta:
		model = CustomUser
		fields = ('name', 'email', 'phone', 'username', 'address', 'last_login', 'date_joined', 'age', 'dob', 'gender', 'covid_status')
		export_order = ('name', 'email', 'phone', 'username', 'address', 'last_login', 'date_joined', 'age', 'dob', 'gender', 'covid_status')

	# symptoms = Field(
	# 	attribute = 'symptoms',
	# 	widget= ManyToManyWidget(UserQuarantineSymptomsData, 'id')
	# 	)
	
	def dehydrate_covid_status(self, obj):
		return obj.covid_status()

	# def dehydrate_answers(self, obj):

	# 	return ""


class SymptomsInline(admin.TabularInline):
	model = UserQuarantineSymptomsData
	exclude = ('result', )
	extra = 0
	verbose_name = "User Symptoms Data"
	readonly_fields = ('data', )
	
	def has_add_permission(self, request, obj):
		return False

	def has_delete_permission(self, request, obj):
		return False

# class CustomerUserAdmin(ExportMixin, admin.ModelAdmin):
class CustomerUserAdmin(ExportMixin, admin.ModelAdmin):
	list_filter = (CovidPositiveFilter,)
	list_display = ('name', 'phone', 'covid_status')
	_exclude = ('password', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'user_permissions', 'groups', 'last_login')
	# fields = ['covid_status', 'username', 'is_active', 'date_joined', 'name', 'email', 'phone', 'address', 'age', 'dob', 'gender', 'Volunteer', ]
	resource_class = CustomUserResource
	inlines = [
		SymptomsInline,
	]
	readonly_fields = ('covid_status', )

	def get_export_formats(self):
		formats = (
		      FORMATS.base_formats.CSV,
		      FORMATS.base_formats.XLS,
		      FORMATS.base_formats.XLSX,
		)
		return [f for f in formats if f().can_export()]

	def get_fields(self, request, obj=None):    
		fields = super().get_fields(request, obj)
		fields.remove('covid_status')
		fields = ['covid_status'] + fields
		return fields

	def get_form(self, request, obj=None, **kwargs):
		self.exclude = []
		if not request.user.is_superuser:
			self.exclude.extend(self._exclude) #here!
		# else:
		# 	self.fields.extend(self._exclude)
		
		return super(CustomerUserAdmin, self).get_form(request, obj, **kwargs)





admin.site.site_header = "COVID 19"

admin.site.site_title = 'COVID 19 ADMIN'
admin.site.site_url = '/'
admin.empty_value_display = '**Empty**'

# admin.site.register(CoronaHospital)
# admin.site.register(UserQuarantineData)
admin.site.register(Role)
admin.site.register(CustomUser, CustomerUserAdmin)
admin.site.register(NewsFeed)
admin.site.register(CovidInitialQuestions)
admin.site.register(Choice)

admin.site.register(CovidInitialQuestionsResponse)

admin.site.register(UserFireBaseDeviceToken)


admin.site.register(QuarantineSymptomsChoices)
admin.site.register(QuarantineSymptomsQuestions)
admin.site.register(UserQuarantineSymptomsData)
admin.site.register(Message)

admin.site.register(DropdownValues)

admin.site.register(Links)