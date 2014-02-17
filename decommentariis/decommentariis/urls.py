from django.conf.urls import *
from django.contrib.auth.models import User, Group
from decommentariis.api import TEIEntryResource
from django.contrib import admin

admin.autodiscover()

#tei_source = TEIDataSourceResource()
tei_resource = TEIEntryResource()

urlpatterns = patterns('',
	# Examples:
	# url(r'^admin/', include(admin.site.urls)),
	#(r'^blog/', include('decommentariis.urls')),
    (r'^api/', include(tei_resource.urls)),
)


