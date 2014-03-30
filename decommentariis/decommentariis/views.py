import datetime
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from decommentariis.models import TEIEntry, TEISection
from decommentariis.models import Cohort, CohortMembers, CohortTexts
from decommentariis.xml_file import TEIDataSource
from decommentariis.forms import UserForm, CohortEditForm, CohortCreateForm

class TextListView(ListView) :
	model = TEIEntry
	template_name = 'text_list.html'
	paginate_by = 25
	selected_author = None

	def get_context_data(self, **kwargs) :
		context = super(TextListView, self).get_context_data(**kwargs)
		authorsqueryset = TEIEntry.objects.exclude(author=None).order_by('author').values_list('author', flat=True).distinct()
		context['author_list'] = authorsqueryset
		context['selected_author'] = self.selected_author
		return context

	def get_queryset(self) :
		if 'author' in self.request.GET and self.request.GET['author'] :
			self.selected_author = self.request.GET['author']
			self.paginate_by = 0
			return TEIEntry.objects.filter(author=self.selected_author)
		else :
			self.paginate_by = 25
			return TEIEntry.objects.all()


class SectionListView(ListView) :
	template_name = 'section_list.html'
	paginate_by = 25

	def get_queryset(self) :
		urn = self.kwargs['urn']
		self.teientry = TEIEntry.objects.get(cts_urn=urn)
		## self.teientry = get_object_or_404(TEIEntry, cts_urn=urn)
		return TEISection.objects.filter(entry=self.teientry)

	def get_context_data(self, **kwargs) :
		# Call the base implementation first to get a context
		context = super(SectionListView, self).get_context_data(**kwargs)
		context['teientry'] = self.teientry
		return context

class SectionTextDetailView(DetailView) :
	template_name = 'section_text.html'

	def get_queryset(self) :
		urn = self.kwargs['urn']
		return TEISection.objects.filter(cts_urn=urn)

	def get_object(self) :
		urn = self.kwargs['urn']
		return TEISection.objects.get(cts_urn=urn)

	def get_context_data(self, **kwargs) :
		context = super(SectionTextDetailView, self).get_context_data(**kwargs)
		context['section_text'] = self.object.readData()
		context['section_path'] = self.object.parents()
		siblings = self.object.siblings()
		if 'prev' in siblings :
			context['section_prev'] = siblings['prev']
		if 'next' in siblings :
			context['section_next'] = siblings['next']
		context['children'] = self.object.children()
		return context

class CohortListView(ListView) :
	template_name = 'cohort/cohort_list.html'
	model = Cohort
	paginate_by = 25
	selected_instructor = None

	def get_context_data(self, **kwargs) :
		context = super(CohortListView, self).get_context_data(**kwargs)
		instructorsqueryset = Cohort.objects.exclude(instructor=None).order_by('instructor__username').values_list('instructor__username', flat=True).distinct()
		context['instructor_list'] = instructorsqueryset
		context['selected_instructor'] = self.selected_instructor
		return context

	def get_queryset(self) :
		if 'instructor' in self.request.GET and self.request.GET['instructor'] :
			self.selected_instructor = self.request.GET['instructor']
			self.paginate_by = 0
			return Cohort.objects.filter(instructor__username=self.selected_instructor)
		else :
			self.paginate_by = 25
			return Cohort.objects.all()

class CohortDetailView(UpdateView) :
	template_name = 'cohort/cohort_detail.html'
	success_url = './'
	context_object_name = 'cohort'
	model = Cohort
	form_class = CohortEditForm
	fields = ['cohort_description']

	def form_valid(self, form) :
		if form.instance.instructor != self.request.user :
			raise ValidationError('Action is not allowed by user {0}'.format(self.request.user.username))
		return super(CohortDetailView, self).form_valid(form)

class CohortCreate(CreateView) :
	model = Cohort
	fields = ['cohort_name', 'cohort_description']
	form_class = CohortCreateForm
	template_name = 'cohort/cohort_new.html'
	
	def form_valid(self, form) :
		form.instance.instructor = self.request.user
		return super(CohortCreate, self).form_valid(form)


## old school views

def main_page(request) :
	return render_to_response('index.html')

def about_page(request) :
	return render_to_response('about.html')
	
def contact_page(request) :
	return render_to_response('contact.html')

def logout_page(request) :
	"""
	Log users out and re-direct them to the main page.
	"""
	logout(request)
	return HttpResponseRedirect('/')





