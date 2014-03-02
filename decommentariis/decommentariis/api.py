# decommentariis/api.py
from tastypie import fields
from tastypie.resources import Resource, ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication, SessionAuthentication, MultiAuthentication 
from tastypie.authorization import DjangoAuthorization
from decommentariis.models import TEIEntry, TEISection, CommentaryEntry
from django.contrib.auth.models import User

class TEIEntryResource(ModelResource):
	sections = fields.ToManyField('decommentariis.api.TEISectionResource', 'teisection_set', related_name='entry')
	class Meta:
		queryset = TEIEntry.objects.all()
		resource_name = 'sourcetext'
		excludes = ['metadata']
		list_allowed_methods = ['get']

	def dehydrate(self, bundle):
		bundle.data['section_refs'] = bundle.obj.section_refs()
		return bundle

class TEISectionResource(ModelResource):
	entry = fields.ForeignKey(TEIEntryResource, 'entry', related_name='sections')
	user_commentaries = fields.ToManyField('decommentariis.api.CommentaryEntryResource', 'commentaryentry_set', related_name='section')

	class Meta:
		queryset = TEISection.objects.all()
		resource_name = 'sourcesection'
		list_allowed_methods = ['get']

	def dehydrate(self, bundle):
		#bundle.data['text_data'] = bundle.obj.readData()
		return bundle 

class CommentaryEntryResource(ModelResource):
	section = fields.ForeignKey(TEISectionResource, 'section', related_name='user_commentaries')
	user = fields.ForeignKey('decommentariis.api.UserResource', 'user')

	class Meta:
		queryset = CommentaryEntry.objects.all()
		resource_name = 'sourcecommentary'
		list_allowed_methods = ['get', 'put', 'post']
		authentication = SessionAuthentication()
		authorization = DjangoAuthorization()
		filtering = {
			'section': ALL_WITH_RELATIONS,
			'user': ALL_WITH_RELATIONS,
		}

	def dehydrate(self, bundle):
		# bundle.data['text_data'] = bundle.obj.readData()
		return bundle 

class UserResource(ModelResource):
	pass
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		list_allowed_methods = ['get']
		fields = ['username', 'first_name', 'last_name', 'id']
		authentication = SessionAuthentication()
		authorization = DjangoAuthorization()
		filtering = {
			'username': ALL,
		}

