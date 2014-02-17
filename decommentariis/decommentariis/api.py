# decommentariis/api.py
from tastypie import fields
from tastypie.resources import ModelResource
from decommentariis.models import TEIEntry

class TEIEntryResource(ModelResource):
    class Meta:
        queryset = TEIEntry.objects.all()
        resource_name = 'teientry'
