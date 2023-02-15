from django.contrib import admin
from .models import Prefeitura, Secretaria, Setor, Colaborador,Documento


# Register your models here.
admin.site.register(Prefeitura)
admin.site.register(Secretaria)
admin.site.register(Setor)
admin.site.register(Colaborador)
admin.site.register(Documento)
