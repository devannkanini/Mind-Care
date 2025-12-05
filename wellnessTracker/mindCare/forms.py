from django.forms import ModelForm
from django import forms
from .models import Issue, RequestHelp



class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'category', ]
 
class HelpRequestForm(forms.ModelForm):
    class Meta:
        model = RequestHelp
        fields = ['professional_name', 'issue_title', 'issue_description']