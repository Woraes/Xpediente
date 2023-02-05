from unicodedata import name
from django.urls import path
from .views import Home, PrefeituraNew, PrefeituraLista,PrefeituraUpdate,PrefeituraDelete






urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('prefeitura_new/', PrefeituraNew.as_view(), name='prefeitura_new'),
    path('prefeitura_lista/', PrefeituraLista.as_view(), name='prefeitura_lista'),
    path('prefeitura_update/<int:pk>', PrefeituraUpdate.as_view(), name='prefeitura_update'),
    path('prefeitura_delete/<int:pk>', PrefeituraDelete.as_view(), name='prefeitura_delete'),

     
]