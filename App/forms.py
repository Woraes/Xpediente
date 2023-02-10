from django import forms

from App.models import Prefeitura


class FormSecretaria(forms.Form):
    prefeitura = forms.ModelChoiceField(queryset=Prefeitura.objects.all())