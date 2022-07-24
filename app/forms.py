from django import forms


class PDFForm(forms.Form):
    pdf = forms.FileField(
        widget=forms.FileInput(attrs={'style': 'display:none;', 'id': 'file', 'multiple': True, 'name': 'files'}))
