from unicodedata import name
from django.urls import path
from .views import Home, PrefeituraNew, PrefeituraLista,PrefeituraUpdate,PrefeituraDelete,SecretariaNew,SecretariaLista
from .views import GerarPdfView
from .views import prefeitura_view,SecretariaUpdate




urlpatterns = [
    path('', Home.as_view(), name='home'),
    
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

]