import datetime
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from decommentariis.models import TEIEntry, TEISection
from decommentariis.xml_file import TEIDataSource
from decommentariis.forms import UserForm

class TextListView(ListView):
	model = TEIEntry
	template_name = 'text_list.html'

class SectionListView(ListView):
	template_name = 'section_list.html'

	def get_queryset(self):
		urn = self.kwargs['urn']
		self.teientry = TEIEntry.objects.get(cts_urn=urn)
		## self.teientry = get_object_or_404(TEIEntry, cts_urn=urn)
		return TEISection.objects.filter(entry=self.teientry)

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(SectionListView, self).get_context_data(**kwargs)
		context['teientry'] = self.teientry
		return context

class SectionTextDetailView(DetailView):
	template_name = 'section_text.html'

	def get_queryset(self):
		urn = self.kwargs['urn']
		return TEISection.objects.filter(cts_urn=urn)

	def get_object(self):
		urn = self.kwargs['urn']
		return TEISection.objects.get(cts_urn=urn)

	def get_context_data(self, **kwargs):
		context = super(SectionTextDetailView, self).get_context_data(**kwargs)
		context['section_text'] = self.object.readData()
		context['section_path'] = self.object.parents()
		siblings = self.object.siblings()
		if 'prev' in siblings:
			print('prev whiizo')
			context['section_prev'] = siblings['prev']
		if 'next' in siblings:
			context['section_next'] = siblings['next']
		context['children'] = self.object.children()
		return context


## old school views

def main_page(request):
    return render_to_response('index.html')

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')





