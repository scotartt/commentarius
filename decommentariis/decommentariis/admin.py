from django.contrib import admin
from decommentariis.models import TEIEntry

class TEIEntryAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(TEIEntry, TEIEntryAdmin)
