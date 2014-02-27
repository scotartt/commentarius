from django import forms
from django.contrib.auth.models import User
from decommentariis.models import CommentaryEntry, TEIEntry, TEISection

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

