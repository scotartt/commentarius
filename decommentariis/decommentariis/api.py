# decommentariis/api.py
from django.contrib.auth.models import User
import markdown
import bleach
from tastypie import fields
from tastypie.resources import Resource, ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication, SessionAuthentication, MultiAuthentication 
from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from decommentariis.models import TEIEntry, TEISection, CommentaryEntry, CommentaryEntryVoter
from decommentariis.api_authorization import UpdateUserObjectsOnlyAuthorization

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
		filtering = {
			'cts_urn': ALL,
		}

	def dehydrate(self, bundle):
		#bundle.data['text_data'] = bundle.obj.readData()
		return bundle 

class CommentaryEntryResource(ModelResource):
	section = fields.ForeignKey(TEISectionResource, 'section', related_name='user_commentaries')
	user = fields.ForeignKey('decommentariis.api.UserResource', 'user')
	voters = fields.ToManyField('decommentariis.api.CommentaryEntryVoterResource', 'commentaryentryvoter_set', related_name='entry')

	class Meta:
		queryset = CommentaryEntry.objects.all()
		resource_name = 'sourcecommentary'
		list_allowed_methods = ['get', 'put', 'post']
		authentication = SessionAuthentication()
		authorization = UpdateUserObjectsOnlyAuthorization()
		filtering = {
			'section': ALL_WITH_RELATIONS,
			'user': ALL_WITH_RELATIONS,
			'voters': ALL_WITH_RELATIONS,
		}

	def dehydrate(self, bundle):
		bundle.data['commentary.html'] = markdown.markdown(bundle.obj.commentary, encoding="utf-8", output_format="html5", safe_mode=False)
		bundle.data['commentary.md'] = bundle.obj.commentary
		return bundle 

class CommentaryEntryVoterResource(ModelResource):
	voter = fields.ForeignKey('decommentariis.api.UserResource', 'user')
	entry = fields.ForeignKey(TEIEntryResource, 'entry', related_name='voters')
	class Meta:
		queryset = CommentaryEntryVoter.objects.all()
		resource_name = "voter"
		list_allowed_methods = ['get', 'post', 'delete']
		authentication = SessionAuthentication()
		authorization = UpdateUserObjectsOnlyAuthorization()
		filtering = {
			'entry': ALL_WITH_RELATIONS,
			'voter': ALL_WITH_RELATIONS,
		}


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

