from django.conf.urls import *
from django.contrib.auth.models import User, Group
from django.contrib import admin
from tastypie.api import Api
from decommentariis.api import TEIEntryResource, TEISectionResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(TEIEntryResource())
v1_api.register(TEISectionResource())

urlpatterns = patterns('',
	# Examples:
	(r'^admin/', include(admin.site.urls)),
	(r'^api/', include(v1_api.urls)),
)
