from django.contrib import admin
from django.contrib.sites.models import Site
from decommentariis.models import TEIEntry, TEISection, CommentaryEntry

class TEIEntryAdmin(admin.ModelAdmin):
	pass

class TEISectionAdmin(admin.ModelAdmin):
	pass


class CommentaryEntryAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(TEIEntry, TEIEntryAdmin)
admin.site.register(TEISection, TEISectionAdmin)
admin.site.register(CommentaryEntry, CommentaryEntryAdmin)
