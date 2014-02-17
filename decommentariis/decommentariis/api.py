# decommentariis/api.py
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from decommentariis.models import Entry

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'


class EntryResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'

# class TEIDataSourceResource(ModelResource):
#     class Meta:
#         #queryset = TEIDataSource.list()
#         resource_name = 'teidocs'
