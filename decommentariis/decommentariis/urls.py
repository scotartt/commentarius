from django.conf.urls import *
from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from tastypie.api import Api
from decommentariis.api import TEIEntryResource, TEISectionResource, CommentaryEntryResource, UserResource
from decommentariis.views import main_page, logout_page, TextListView, SectionListView, SectionTextDetailView
#from decommentariis.views import TextListView, SectionListView, SectionTextDetailView

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(TEIEntryResource())
v1_api.register(TEISectionResource())
v1_api.register(CommentaryEntryResource())
v1_api.register(UserResource())

urlpatterns = patterns('',
	(r'^$', main_page),
	# Login / logout.
	#(r'^login/$', 'django.contrib.auth.views.login'),
)

urlpatterns += patterns('decommentariis.views',
	# a CTS URN looks like this 'urn:cts:latinLit:phi0631.phi001.perseus-lat2'
	url(r'^text/$', TextListView.as_view()),
	url(r'^text/(?P<urn>urn:cts:([a-z]{5})Lit:([a-zA-Z]{3,4}\d{3,4}\.){2}[\w-]+)/$', SectionListView.as_view()),
	url(r'^textdata/(?P<urn>urn:cts:([a-z]{5})Lit:([a-zA-Z]{3,4}\d{3,4}\.){2}[\w-]+:[\w\., ()]+)/$', login_required(SectionTextDetailView.as_view())),
)

# urlpatterns += patterns('',
# 	url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
# )

urlpatterns += patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include(v1_api.urls)),
)

urlpatterns += patterns('',
	(r'^logout/$', logout_page),
	(r'^accounts/', include('allauth.urls')),
)
