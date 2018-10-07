from django import forms


class CodeForm(forms.Form):
    code = forms.CharField(required=True, widget=forms.Textarea)
