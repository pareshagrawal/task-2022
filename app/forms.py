from django import forms

class ValidGitUrl(forms.Form):
    url = forms.CharField(required=True)