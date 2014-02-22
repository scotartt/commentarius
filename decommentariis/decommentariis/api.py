# decommentariis/api.py
from tastypie import fields
from tastypie.resources import ModelResource
from decommentariis.models import TEIEntry, TEISection

class TEIEntryResource(ModelResource):
	class Meta:
		queryset = TEIEntry.objects.all()
		resource_name = 'sourcetext'
		excludes = ['metadata']
		list_allowed_methods = ['get']
		# authorization = DjangoAuthorization()
		# filtering = {
		#     'slug': ALL,
		#     'user': ALL_WITH_RELATIONS,
		#     'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
		# }

class TEISectionResource(ModelResource):
	entry = fields.ForeignKey(TEIEntryResource, 'entry')

	class Meta:
		queryset = TEISection.objects.all()
		resource_name = 'sourcesection'
		list_allowed_methods = ['get']

