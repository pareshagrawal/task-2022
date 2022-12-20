from django import forms

class ValideGitUrl(forms.Form):
    url = forms.CharField(required=True)