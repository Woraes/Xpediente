from django import forms
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
import requests



# Create your models here.

class Prefeitura(models.Model):
    nome = models.CharField(max_length=30, blank=False, null=True, unique=True, verbose_name='Nome da Prefeitura')
    criadopor = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return '{} - Criado por:({}) '.format(self.nome, self.criadopor)
        
      
        
        
class Secretaria(models.Model):
    nome = models.CharField(max_length=40, blank=False, null=True, verbose_name='Nome do setor')
    sigla = models.CharField(max_length=7, blank=False, null=True, verbose_name='Sigla do Setor')
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$") # regex validação
    telefone = models.CharField(validators = [phoneNumberRegex],max_length=17, blank=False, null=True, verbose_name='Telefone', )
    status =models.CharField(max_length=10, blank=False, null=True, verbose_name='Status', 
        choices=(
         ( 'ATIVO' ,  'ATIVO' ),
         ( 'INATIVO' ,  'INATIVO' ),
        ))
    cep = models.CharField(max_length=8, blank=False, null=True, verbose_name='cep')
    logradouro = models.CharField(max_length=70, blank=True, null=True, verbose_name='logradouro')

    def buscar_cep(cep):
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        endereco = response.json()
        return endereco

    def save(self, *args, **kwargs):
        endereco = self.buscar_cep(self.cep)
        self.logradouro = endereco["logradouro"]
        super().save(*args, **kwargs)

    complemento = models.CharField(max_length=70, blank=True, null=True, verbose_name='complemento')
    bairro = models.CharField(max_length=70, blank=True, null=True, verbose_name='bairro')
    localidade = models.CharField(max_length=70, blank=True, null=True, verbose_name='localidade')
    complemento = models.CharField(max_length=70, blank=True, null=True, verbose_name='complemento')
    uf = models.CharField(max_length=70, blank=True, null=True, verbose_name='uf')
    uf = models.CharField(max_length=10, blank=False, null=True, verbose_name='UF', 
        choices=(
        ("AC", "Acre"), 
		("AL", "Alagoas"),
		("AM", "Amazonas"),
		("BA", "Bahia"),
		("CE", "Ceará"),
		("DF", "Distrito Federal"),
		("ES", "Espírito Santo"),
		("GO", "Goiás"),
		("MA", "Maranhão"),
		("MT", "Mato Grosso"),
		("MS", "Mato Grosso do Sul"),
		("MG", "Minas Gerais"),
		("PA", "Pará"),
		("PB", "Paraíba"),
		("PR", "Paraná"),
		("PE", "Pernambuco"),
		("PI", "Piauí"),
		("RJ", "Rio de Janeiro"),
		("RN", "Rio Grande do Norte"),
		("RS", "Rio Grande do Sul"),
		("RO", "Rondônia"),
		("RR", "Roraima"),
		("SC", "Santa Catarina"),
		("SP", "São Paulo"),
		("SE", "Sergipe"),
		("TO", "Tocantins"),
        ))
    criadopor = models.ForeignKey(User, on_delete=models.PROTECT)

   
    
    def __str__(self):
        return '{} ({}) criado por {}'.format(self.sigla, self.nome, self.criadopor)        