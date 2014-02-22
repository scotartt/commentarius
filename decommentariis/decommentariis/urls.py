from django.conf.urls import *
from django.contrib.auth.models import User, Group
from django.contrib import admin
from tastypie.api import Api
from decommentariis.api import TEIEntryResource, TEISectionResource
from decommentariis.views import TextListView, SectionListView

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(TEIEntryResource())
v1_api.register(TEISectionResource())

urlpatterns = patterns('decommentariis.views',
	# a CTS URN looks like this 'urn:cts:latinLit:phi0631.phi001.perseus-lat2'
	url(r'^text/$', TextListView.as_view()),
	url(r'^text/(?P<urn>urn:cts:([a-z]{5})Lit:([a-zA-Z]{3,4}\d{3,4}\.){2}[\w-]+)/$', SectionListView.as_view()),
)

urlpatterns += patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include(v1_api.urls)),
)
