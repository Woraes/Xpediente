from django.db import models
from django.contrib.auth.models import User

from App.models import Prefeitura, Secretaria, Setor

# Create your models here.
class Perfil(models.Model):
    nome = models.CharField(max_length=55, blank=False, null=True, verbose_name='Nome Completo')
    cpf = models.CharField(max_length=14, blank=False, null=True, verbose_name='CPf')
    matricula = models.CharField(max_length=20, blank=False, null=True, verbose_name='Matrícula')
    telefone = models.CharField(max_length=20, blank=False, null=True, verbose_name='Telefone')
    email = models.EmailField(max_length=100, blank=False, null=True, verbose_name='Email')
    foto = models.ImageField(("Sua Foto"), upload_to='userfoto/', height_field=None, width_field=None, max_length=None)
    cep = models.CharField(max_length=20, blank=False, null=True, verbose_name='Cep')
    prefeitura = models.ForeignKey(Prefeitura, on_delete=models.CASCADE, verbose_name='Prefeitura')
    secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE, verbose_name='Secretária')
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, verbose_name='Setor')
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    
    def __str__(self):
         return 'Nome: ({}) - Criado por:({}) '.format(self.nome,self.usuario)     


