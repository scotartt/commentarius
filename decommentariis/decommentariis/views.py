import datetime
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from decommentariis.models import TEIEntry, TEISection
from decommentariis.xml_file import TEIDataSource

class TextListView(ListView):
	model = TEIEntry
	template_name = 'text_list.html'

class SectionListView(ListView):
	template_name = 'section_list.html'

	def get_queryset(self):
		urn = self.kwargs['urn']
		self.teitext = TEIEntry.objects.get(cts_urn=urn)
		## self.teitext = get_object_or_404(TEIEntry, cts_urn=urn)
		return TEISection.objects.filter(entry=self.teitext)

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(SectionListView, self).get_context_data(**kwargs)
		context['teitext'] = self.teitext
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
		return context







