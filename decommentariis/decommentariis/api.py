# decommentariis/api.py
from tastypie import fields
from tastypie.resources import Resource, ModelResource
from decommentariis.models import TEIEntry, TEISection, TEISectionText

class TEIEntryResource(ModelResource):
	sections = fields.ToManyField('decommentariis.api.TEISectionResource', 'teisection_set', related_name='entry')
	class Meta:
		queryset = TEIEntry.objects.all()
		resource_name = 'sourcetext'
		excludes = ['metadata']
		list_allowed_methods = ['get']

class TEISectionResource(ModelResource):
	entry = fields.ForeignKey(TEIEntryResource, 'entry', related_name='sections')

	class Meta:
		queryset = TEISection.objects.all()
		resource_name = 'sourcesection'
		list_allowed_methods = ['get']
