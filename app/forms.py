from django import forms


class MergeForm(forms.Form):
    pdf = forms.FileField(
        widget=forms.FileInput(attrs={'style': 'display:none;', 'id': 'file', 'multiple': True, 'accept': '.pdf'}))


class SplitForm(forms.Form):
    pdf = forms.FileField(
        widget=forms.FileInput(attrs={'style': 'display:none;', 'id': 'file', 'accept': '.pdf'}))


class PdfToWordForm(forms.Form):
    pdf = forms.FileField(
        widget=forms.FileInput(attrs={'style': 'display:none;', 'id': 'file', 'accept': '.pdf'}))
