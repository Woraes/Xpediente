from django import forms
from django.forms import ModelForm

from App.models import Documento, Prefeitura, Secretaria,Setor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Row
from crispy_forms.layout import Field
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

# class FormPrefeitura(forms.Form):
#     class Meta:
#         prefeitura = forms.CharField(label='Prefeitura', max_length=30)
        



    
class FormSecretaria(forms.ModelForm):
    class Meta:
        model = Secretaria
        fields = [
            'nome',
            'prefeitura',
            'sigla',
            'telefone',
            'status',
            'cep',
            'logradouro',
            'complemento',
            'bairro',
            'localidade',
            'uf',
            
        ]
        

            
            
        
        
