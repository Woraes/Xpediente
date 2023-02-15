from unicodedata import name
from django.urls import path
from .views import Home, PrefeituraNew, PrefeituraLista,PrefeituraUpdate,PrefeituraDelete,SecretariaNew,SecretariaLista
from .views import GerarPdfView
from .views import prefeitura_view,SecretariaUpdate,SecretariaDelete,SetorNew,SetorLista, SetorUpdate,SetorDelete
from .views import ColaboradorNew,ColaboradorLista,ColaboradorUpdate,ColaboradorDelete
from .views import DocumentoNew
from .views import requisicao_api
from django.contrib.auth import views as auth_views

from . import views



urlpatterns = [
    #Paginas
    path('', Home.as_view(), name='home'),
    
    #def
    path('requisicao_api', views.requisicao_api, name='requisicao_api'), 
       
    #Prefeitura
    path('prefeitura_new/', PrefeituraNew.as_view(), name='prefeitura_new'),
    path('prefeitura_lista/', PrefeituraLista.as_view(), name='prefeitura_lista'),
    path('prefeitura_update/<int:pk>', PrefeituraUpdate.as_view(), name='prefeitura_update'),
    path('prefeitura_delete/<int:pk>', PrefeituraDelete.as_view(), name='prefeitura_delete'),
    path('viewpdf', prefeitura_view, name='viewpdf'),
    
    #Secretaria
    path('secretaria_new/', SecretariaNew.as_view(), name='secretaria_new'),
    path('secretaria_lista/', SecretariaLista.as_view(), name='secretaria_lista'),
    path('secretaria_update/<int:pk>', SecretariaUpdate.as_view(), name='secretaria_update'),
    path('secretaria_delete/<int:pk>', SecretariaDelete.as_view(), name='secretaria_delete'),

    #Setor
    path('setor_new/', SetorNew.as_view(), name='setor_new'),
    path('setor_lista/', SetorLista.as_view(), name='setor_lista'),
    path('setor_update/<int:pk>', SetorUpdate.as_view(), name='setor_update'),
    path('setor_delete/<int:pk>', SetorDelete.as_view(), name='setor_delete'),

    #Colaborador
    path('colaborador_new/', ColaboradorNew.as_view(), name='colaborador_new'),
    path('colaborador_lista/', ColaboradorLista.as_view(), name='colaborador_lista'),
    path('colaborador_update/<int:pk>', ColaboradorUpdate.as_view(), name='colaborador_update'),
    path('colaborador_delete/<int:pk>', ColaboradorDelete.as_view(), name='colaborador_delete'),

    #Documentos
    path('documento_new/', DocumentoNew.as_view(), name='documento_new'),


]