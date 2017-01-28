# decommentariis.resources

import markdown
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from decommentariis.api.api_authorization import UpdateUserObjectsOnlyAuthorization
from decommentariis.api.api_authorization import CohortInstructorOrMemberAuthorization
from decommentariis.api.api_authorization import UserObjectsOnlyAuthorization
from decommentariis.models import Cohort, CohortMembers
from decommentariis.models import TEIEntry, TEISection, CommentaryEntry, CommentaryEntryVoter


class TEIEntryResource(ModelResource):
	sections = fields.ToManyField('decommentariis.api.resources.TEISectionResource', 'teisection_set', related_name='entry')
	
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
	user_commentaries = fields.ToManyField(
		'decommentariis.api.resources.CommentaryEntryResource',
		'commentaryentry_set', related_name='section')

	class Meta:
		queryset = TEISection.objects.all()
		resource_name = 'sourcesection'
		list_allowed_methods = ['get']
		filtering = {
			'cts_urn': ALL,
		}

	def dehydrate(self, bundle):
		# bundle.data['text_data'] = bundle.obj.readData()
		return bundle 


class CommentaryEntryResource(ModelResource):
	section = fields.ForeignKey(TEISectionResource, 'section', related_name='user_commentaries')
	user = fields.ForeignKey('decommentariis.api.resources.UserResource', 'user')
	voters = fields.ToManyField(
		'decommentariis.api.resources.CommentaryEntryVoterResource',
		'commentaryentryvoter_set',
		related_name='entry', null=True, full=True)
	print("hello")
	
	class Meta:
		queryset = CommentaryEntry.objects.all()
		resource_name = 'sourcecommentary'
		list_allowed_methods = ['get', 'put', 'post', 'delete']
		authentication = SessionAuthentication()
		# authorization = UpdateUserObjectsOnlyAuthorization()
		authorization = Authorization()
		filtering = {
			'section': ALL_WITH_RELATIONS,
			'user': ALL_WITH_RELATIONS,
			'id': ALL,
		}

	def dehydrate(self, bundle):
		print("dehydrating " + bundle)
		bundle.data['commentary.html'] = markdown.markdown(
			bundle.obj.commentary,
			encoding="utf-8", output_format="html5", safe_mode=False)
		bundle.data['commentary.md'] = bundle.obj.commentary
		return bundle 


class CommentaryEntryVoterResource(ModelResource):
	voter = fields.ForeignKey('decommentariis.api.resources.UserResource', 'user')
	entry = fields.ForeignKey(CommentaryEntryResource, 'entry', related_name='voters')
	
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


class CohortResource(ModelResource):
	instructor = fields.ForeignKey('decommentariis.api.resources.UserResource', 'instructor')
	members = fields.ToManyField(
		'decommentariis.api.resources.CohortMembersResource',
		'cohortmembers_set',
		related_name='cohort', null=True, full=False
	)
	
	class Meta:
		queryset = Cohort.objects.all()
		resource_name = 'cohort'
		list_allowed_methods = ['get', 'post', 'delete']
		fields = ['cohort_name', 'cohort_description', 'instructor', 'creation_date']
		authentication = SessionAuthentication()
		authorization = CohortInstructorOrMemberAuthorization()


class CohortMembersResource(ModelResource):
	cohort = fields.ForeignKey('decommentariis.api.resources.CohortResource', 'cohort', related_name='members')
	member = fields.ForeignKey('decommentariis.api.resources.UserResource', 'member')
	
	class Meta:
		queryset = CohortMembers.objects.all()
		resource_name = 'cohortmember'
		list_allowed_methods = ['get', 'post', 'delete']
		authentication = SessionAuthentication()
		authorization = CohortInstructorOrMemberAuthorization()
		filtering = {
			'cohort': ALL_WITH_RELATIONS,
			'member': ALL_WITH_RELATIONS,
		}
