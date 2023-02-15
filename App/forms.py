from django import forms
from django.forms import ModelForm

from App.models import Prefeitura, Secretaria
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Row
from crispy_forms.layout import Field

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
        
    def __init__(self, *args, **kwargs):
        super(FormSecretaria, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                Field('nome', css_class='form-group col-md-6'),
                Field('prefeitura', css_class='form-group col-md-6'),
            )
            
            
        
        
