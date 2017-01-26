from django import forms
from django.contrib import admin
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from decommentariis.models import TEIEntry, TEISection, CommentaryEntry, CommentaryEntryVoter


class TEIEntryAdmin(admin.ModelAdmin):
	pass


class TEISectionAdmin(admin.ModelAdmin):
	pass


class CommentaryEntryAdmin(admin.ModelAdmin):
	fields = ['user', 'section', 'creation_date', 'votes', 'commentary']


class CommentaryEntryVoterAdmin(admin.ModelAdmin):
	pass


admin.site.register(TEIEntry, TEIEntryAdmin)
admin.site.register(TEISection, TEISectionAdmin)
admin.site.register(CommentaryEntry, CommentaryEntryAdmin)
admin.site.register(CommentaryEntryVoter, CommentaryEntryVoterAdmin)


class GroupAdminForm(forms.ModelForm):
	users = forms.ModelMultipleChoiceField(
		queryset=User.objects.all(), 
		required=False,
		widget=FilteredSelectMultiple(
			verbose_name=_('Users'),
			is_stacked=False
		),
	)
	
	class Meta:
		model = Group
		fields = '__all__'
	
	def __init__(self, *args, **kwargs):
		super(GroupAdminForm, self).__init__(*args, **kwargs)

		if self.instance and self.instance.pk:
			self.fields['users'].initial = self.instance.user_set.all()

	def save(self, commit=True):
		group = super(GroupAdminForm, self).save(commit=False)

		if commit:
			group.save()

		if group.pk:
			group.user_set = self.cleaned_data['users']
			self.save_m2m()

		return group


class GroupAdmin(admin.ModelAdmin):
	form = GroupAdminForm
	

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
