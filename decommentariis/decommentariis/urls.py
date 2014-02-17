from django.conf.urls import *
from django.contrib.auth.models import User, Group
from decommentariis.api import EntryResource

from django.contrib import admin
admin.autodiscover()

#tei_source = TEIDataSourceResource()
entry_resource = EntryResource()


urlpatterns = patterns('',
	# Examples:
	# url(r'^admin/', include(admin.site.urls)),
	#(r'^blog/', include('decommentariis.urls')),
    (r'^api/', include(entry_resource.urls)),
)


