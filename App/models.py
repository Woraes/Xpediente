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



            
        


# Prefeitura
class Prefeitura(models.Model):
    nome = models.CharField(max_length=30, blank=False, null=True,  verbose_name='Nome da Prefeitura')
    criadopor = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return '{} - Criado por:({}) '.format(self.nome, self.criadopor)
   
#Secretaria        
class Secretaria(models.Model):
    nome = models.CharField(max_length=40, blank=False, unique=True, null=True, verbose_name='Nome da Secretária')
    prefeitura = models.ForeignKey(Prefeitura, on_delete=models.CASCADE, verbose_name='Prefeitura')
    sigla = models.CharField(max_length=7, blank=False, null=True, verbose_name='Sigla da Secretária')
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$") # regex validação
    telefone = models.CharField(validators = [phoneNumberRegex],max_length=17, blank=False, null=True, verbose_name='Telefone', )
    status =models.CharField(max_length=10, blank=False, null=True, verbose_name='Status', 
        choices=(
         ( 'ativo' ,  'Ativo' ),
         ( 'inativo' , 'Inativo' ),
        ))
    cep = models.CharField(max_length=8, blank=False, null=True, verbose_name='cep')
    logradouro = models.CharField(max_length=70, blank=True, null=True, verbose_name='logradouro')
    complemento = models.CharField(max_length=70, blank=True, null=True, verbose_name='complemento')
    bairro = models.CharField(max_length=70, blank=True, null=True, verbose_name='bairro')
    localidade = models.CharField(max_length=70, blank=True, null=True, verbose_name='localidade')
    uf = models.CharField(max_length=10, blank=True, null=True, verbose_name='uf')
    criadopor = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return '{} - ({}) -- criado por {}'.format(self.sigla, self.nome, self.criadopor)
    

    
#Setor
class Setor(models.Model):
    nome = models.CharField(max_length=40, blank=False, null=True, verbose_name='Nome do setor')
    prefeitura = models.ForeignKey(Prefeitura, on_delete=models.PROTECT, verbose_name='Prefeitura')
    secretaria = models.ForeignKey(Secretaria, on_delete=models.PROTECT, verbose_name='Secretária')
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$") # regex validação
    telefone = models.CharField(validators = [phoneNumberRegex],max_length=17, blank=False, null=True, verbose_name='Telefone', )
    status =models.CharField(max_length=10, blank=False, null=True, verbose_name='Status', 
        choices=(
         ( 'ativo' ,  'Ativo' ),
         ( 'inativo' ,  'Inativo' ),
        ))
    cep = models.CharField(max_length=8, blank=False, null=True, verbose_name='cep')
    logradouro = models.CharField(max_length=70, blank=True, null=True, verbose_name='logradouro')
    complemento = models.CharField(max_length=70, blank=True, null=True, verbose_name='complemento')
    bairro = models.CharField(max_length=70, blank=True, null=True, verbose_name='bairro')
    localidade = models.CharField(max_length=70, blank=True, null=True, verbose_name='localidade')
    uf = models.CharField(max_length=10, blank=True, null=True, verbose_name='uf')
    criadopor = models.ForeignKey(User, on_delete=models.PROTECT)

   
    
    def __str__(self):
        return '{}'.format(self.nome)
    
#Colaborador    
class Colaborador(models.Model):    
        nome = models.CharField(max_length=60, blank=False, unique=True, null=True, verbose_name='Nome')
        nascimento = models.DateField(max_length=9, blank=True, null=True, verbose_name='Nascimento')
        estadocivil = models.CharField(max_length=15, blank=True, null=True, verbose_name='Estadocivil', 
        choices=(              
            ('Solteiro', u'Solteiro'),
            ('Casado', u'Casado'),
            ('Divorciado', u'Divorciado'),
            ('Viúvo', u'Viúvo'),
          ))
        prefeitura = models.ForeignKey(Prefeitura, on_delete=models.CASCADE, verbose_name='Prefeitura')
        secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE, verbose_name='Secretária')
        setor = models.ForeignKey(Setor, on_delete=models.CASCADE, verbose_name='Setor')
        matricula = models.CharField(max_length=15, blank=False,unique=True, null=True, verbose_name='Matrícula')
        rg = models.CharField(max_length=15, blank=True, null=True, verbose_name='Rg')
        cpf = models.CharField(max_length=15, blank=False, null=True, unique=True, verbose_name='CPF')
        pis = models.CharField(max_length=16, blank=True, null=True, unique=True, verbose_name='PIS')
        cns = models.CharField(max_length=16, blank=True, null=True, unique=True, verbose_name='Cns')
        ctps = models.CharField(max_length=7, blank=True, null=True, verbose_name='Ctps número:')
        ctpsserie = models.CharField(max_length=4, blank=True, null=True, verbose_name='Série')
        ctpsuf = models.CharField(max_length=2, blank=True, null=True, verbose_name='UF')
        genero = models.CharField(max_length=16, blank=False, null=True, verbose_name='Genero', 
            choices=(
                ('MASCULINO',  'MASCULINO'),
                ('FEMININO',  'FEMININO'),
                ('NÃO DEFINIDO', 'NÃO DEFINIDO'),                             
            ))
        phone = models.CharField(max_length=16, blank=False,unique=True, null=True, verbose_name='Celular')
        email = models.CharField(max_length=50, blank=False,unique=True, null=True, verbose_name='Email')
        foto = models.ImageField(upload_to='Colaborador_foto', null=True , blank=True, verbose_name='Foto')
        status =models.CharField(max_length=10, blank=False, null=True, verbose_name='Status',
            choices=(
                ( 'ativo' ,  'Ativo' ),
                ( 'inativo' ,  'Inativo' ),
            ))
        dataentrada = models.DateTimeField(max_length=10, blank=False, null=True, verbose_name='Data de Entrada')
        cep = models.CharField(max_length=8, blank=True, null=True, verbose_name='cep')
        logradouro = models.CharField(max_length=70, blank=True, null=True, verbose_name='logradouro')
        complemento = models.CharField(max_length=70, blank=True, null=True, verbose_name='complemento')
        bairro = models.CharField(max_length=70, blank=True, null=True, verbose_name='bairro')
        localidade = models.CharField(max_length=70, blank=True, null=True, verbose_name='localidade')
        uf = models.CharField(max_length=10, blank=True, null=True, verbose_name='uf')
        criadopor = models.ForeignKey(User, on_delete=models.PROTECT)
        
        def __str__(self):
            return '{} - ({}) - ({}) - Criado por:({}) '.format(self.nome, self.cpf, self.matricula, self.criadopor)     
       
       
#Documento   
class Documento(models.Model):    
    nome = models.CharField(max_length=60, blank=False, unique=True, null=True, verbose_name='Nome')
    tipo = models.CharField(max_length=15, blank=False, null=True, verbose_name='Tipo',
        choices=(
                ( 'processo' ,  'Processo' ),
                ( 'requerimeto' ,  'requerimento' ),
                ( 'ata' ,  'Ata' ),
                ( 'ci' ,  'Ci' ),
                ( 'documento' ,  'Documento' ),
            ))
    numeracao = models.CharField(max_length=15, blank=True, null=True, verbose_name='Numeração')
    ano = models.CharField(max_length=15,  blank=True, null=True, verbose_name='Ano')
    assunto = models.TextField(max_length=15, blank=True, null=True, verbose_name='Assunto')
    datainicial = models.DateTimeField(max_length=15, blank=True, null=True, verbose_name='Data Inicial') 
    prefeitura = models.ForeignKey(Prefeitura, on_delete=models.CASCADE, verbose_name='Prefeitura')
    secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE, verbose_name='Secretária')
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, verbose_name='Setor')
    status =models.CharField(max_length=10, blank=False, null=True, verbose_name='Status',
        choices=(
                ( 'ativo' ,  'Ativo' ),
                ( 'inativo' ,  'Inativo' ),
            ))
    anexo = models.FileField(upload_to='', null=True , blank=True, verbose_name='Anexo')

       
    criadopor = models.ForeignKey(User, on_delete=models.PROTECT)
        
    def __str__(self):
            return '{} - ({}) - ({}) - Ano:{}  - Criado por:({}) '.format(self.nome, self.tipo, self.numeracao,self.ano, self.criadopor)       
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
         
           
   
class DocumentoForm(forms.ModelForm):
     
    
    def __init__(self, *args, **kwargs):
        super(DocumentoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        

        # Desabilitando o campo "ano"
        
         
        
    class Meta:
        model = Documento
        fields = '__all__'          