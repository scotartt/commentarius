from django.conf.urls import *
from django.contrib.auth.models import User, Group
from decommentariis.api import TEIEntryResource, TEISectionResource
from django.contrib import admin

admin.autodiscover()

#tei_source = TEIDataSourceResource()
tei_entries = TEIEntryResource()
tei_references = TEISectionResource()

urlpatterns = patterns('',
	# Examples:
	url(r'^admin/', include(admin.site.urls)),
	#(r'^blog/', include('decommentariis.urls')),
    (r'^api/', include(tei_entries.urls)),
    (r'^api/', include(tei_references.urls)),
)


