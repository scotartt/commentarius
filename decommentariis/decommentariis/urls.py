from django.conf.urls import *
from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from django.conf.urls import include, url
from tastypie.api import Api
from decommentariis.api import TEIEntryResource, TEISectionResource, CommentaryEntryResource, UserResource, CommentaryEntryVoterResource, CohortResource, CohortMembersResource
from decommentariis.views import main_page, about_page, contact_page
from decommentariis.views import TextListView, SectionListView, SectionTextDetailView, UserCommentaryView
from decommentariis.views import CohortListView, CohortDetailView, CohortCreate


admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(TEIEntryResource())
v1_api.register(TEISectionResource())
v1_api.register(CommentaryEntryResource())
v1_api.register(UserResource())
v1_api.register(CommentaryEntryVoterResource())
v1_api.register(CohortResource())
v1_api.register(CohortMembersResource())

urlpatterns = [
	url(r'^$', main_page),
	url(r'^about/$', about_page),
	url(r'^about/contact/$', contact_page),
]

urlpatterns += [
	# 'decommentariis.views',
	# a CTS URN looks like this 'urn:cts:latinLit:phi0631.phi001.perseus-lat2'
	url(r'^text/$', TextListView.as_view()),
	url(r'^text/(?P<urn>urn:cts:([a-z]{5})Lit:([a-zA-Z]{3,4}\d{3,4}\w{0,3}\.){2}[\w-]+)/$', SectionListView.as_view()),
	url(r'^textdata/(?P<urn>urn:cts:([a-z]{5})Lit:([a-zA-Z]{3,4}\d{3,4}\w{0,3}\.){2}[\w-]+:[\w\., ()]+)/$',
		login_required(SectionTextDetailView.as_view())),
	url(r'^cohort/$', login_required(CohortListView.as_view()) ),
	url(r'^cohort/(?P<pk>(\w{6,}))/$', login_required(CohortDetailView.as_view()), name='cohort_detail'),
	url(r'^cohort/new/$', login_required(CohortCreate.as_view()), name='cohort_add'),
	url(r'^commentary/$', login_required(UserCommentaryView.as_view()), name='user_commentary_self'),
	url(r'^commentary/(?P<username>([\w\.\-]+))/$', login_required(UserCommentaryView.as_view()),
		name='user_commentary'),
]

# urlpatterns += patterns('',
# 	url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
# )

urlpatterns += [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include(v1_api.urls)),
]

urlpatterns += [
	url(r'^accounts/', include('allauth.urls')),
]
