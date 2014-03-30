import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decommentariis.models import CommentaryEntry, TEIEntry, TEISection
from decommentariis.models import Cohort, CohortMembers, CohortTexts
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import *



class UserForm(forms.ModelForm) :
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta :
		model = User
		fields = ('username', 'email', 'password')
	pass

class CohortCreateForm(forms.ModelForm) :
	cohort_name = forms.CharField(widget=forms.TextInput(), max_length=64)
	cohort_description = forms.CharField(widget=forms.Textarea())
	auto_id = True

	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_id = 'id-cohortform'
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'post'
		self.helper.form_action = 'cohort_add'
		self.helper.html5_required = False
		self.helper.layout = Layout(Field('cohort_name'),
			Field('cohort_description'),
			StrictButton('Create Cohort', type='submit', css_class="btn-success pull-right"))
		super(CohortCreateForm, self).__init__(*args, **kwargs)

	def clean_cohort_name(self) :
		data = self.cleaned_data['cohort_name']
		if re.search(r"[\s\W]+", data) : 
			raise ValidationError('Name must not contain whitespace, and should only contain A-Z, a-z, 0-9, and _ to be valid')
		elif re.search(r"^\d+", data) :
			raise ValidationError('Name must not begin with digits (but may contain them)')
		else :
			return data

	class Meta:
		model = Cohort
		fields = ('cohort_name', 'cohort_description')

class CohortEditForm(forms.ModelForm) :
	#cohort_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), max_length=64)
	cohort_description = forms.CharField(widget=forms.Textarea())
	auto_id = True

	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_id = 'id-cohortform'
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'post'
		# self.helper.form_action = ''
		self.helper.html5_required = False
		self.helper.layout = Layout(
			#Field('cohort_name'),
			Field('cohort_description'),
			StrictButton('Edit Cohort', type='submit', css_class="btn-success pull-right"))
		super(CohortEditForm, self).__init__(*args, **kwargs)

	def clean_cohort_name(self) :
		if self.instance and self.instance.cohort_name and self.instance.cohort_name != self.cleaned_data['cohort_name'] :
			raise ValidationError('Cannot change value of cohort_name')
		elif self.instance and self.instance.cohort_name :
			return self.instance.cohort_name
		else :
			raise ValidationError('Cannot change value of cohort_name')	

	def clean(self) :
		cleaned_data=super(CohortEditForm, self).clean()
		return cleaned_data

	class Meta:
		model = Cohort
		fields = ('cohort_description',)




