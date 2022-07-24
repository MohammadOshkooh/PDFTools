from django import forms


class MergeForm(forms.Form):
    pdf = forms.FileField(
        widget=forms.FileInput(attrs={'style': 'display:none;', 'id': 'file', 'multiple': True,}))


class SplitForm(forms.Form):
    pdf = forms.FileField(
        widget=forms.FileInput(attrs={'style': 'display:none;', 'id': 'file',}))
