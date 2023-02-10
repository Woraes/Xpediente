from django import forms
from django.db import models

from django.contrib.auth.models import User
from django.shortcuts import redirect
import requests
from django.core.validators import RegexValidator


#import validação
from django.contrib import messages


#Crispy form
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Div



            
        


# Create your models here.

class Prefeitura(models.Model):
    nome = models.CharField(max_length=30, blank=False, null=True,  verbose_name='Nome da Prefeitura')
    criadopor = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return '{} - Criado por:({}) '.format(self.nome, self.criadopor)
        
      
        
        
class Secretaria(models.Model):
    nome = models.CharField(max_length=40, blank=False, null=True, verbose_name='Nome da Secretária')
    prefeitura = models.ForeignKey(Prefeitura, on_delete=models.CASCADE, verbose_name='Prefeitura')
    sigla = models.CharField(max_length=7, blank=False, null=True, verbose_name='Sigla da Secretária')
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$") # regex validação
    telefone = models.CharField(validators = [phoneNumberRegex],max_length=17, blank=False, null=True, verbose_name='Telefone', )
    status =models.CharField(max_length=10, blank=False, null=True, verbose_name='Status', 
        choices=(
         ( 'ATIVO' ,  'ATIVO' ),
         ( 'INATIVO' ,  'INATIVO' ),
        ))
    cep = models.CharField(max_length=8, blank=False, null=True, verbose_name='cep')
    logradouro = models.CharField(max_length=70, blank=True, null=True, verbose_name='logradouro')

    # def buscar_cep(cep):
    #     response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    #     endereco = response.json()
    #     return endereco

    # def save(self, *args, **kwargs):
    #     endereco = self.buscar_cep(self.cep)
    #     self.logradouro = endereco["logradouro"]
    #     super().save(*args, **kwargs)

    complemento = models.CharField(max_length=70, blank=True, null=True, verbose_name='complemento')
    bairro = models.CharField(max_length=70, blank=True, null=True, verbose_name='bairro')
    localidade = models.CharField(max_length=70, blank=True, null=True, verbose_name='localidade')
    uf = models.CharField(max_length=10, blank=True, null=True, verbose_name='uf')
    criadopor = models.ForeignKey(User, on_delete=models.PROTECT)

   
    
    def __str__(self):
        return '{} ({}) criado por {}'.format(self.sigla, self.nome, self.criadopor)



    
class FormSecretaria(forms.ModelForm):
    class Meta:
        model = Secretaria
        fields = ['nome',
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
    

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Row(
#                 Div('name', css_class='span6'),
#                 Div('prefeitura', css_class='span6'),
#                 Div('sigla', css_class='span6'),
#                 Div('telefone', css_class='span6'),
#                 Div('status', css_class='span6'),
#                 Div('cep', css_class='span6'),
#                 Div('logradouro', css_class='span6'),
#                 Div('complemento', css_class='span8'),
#                 Div('bairro', css_class='span6'),
#                 Div('localidade', css_class='span6'),
#                 Div('uf', css_class='span6'),
#                 
#                 css_class='row-fluid'
#             ),
#             Submit('submit', 'Enviar')
#         )            