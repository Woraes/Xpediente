from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from braces.views import GroupRequiredMixin
from django.core.paginator import Paginator
import datetime
import requests


#models
from .models import Prefeitura

# Create your views here.



class Home(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = '/Xpediente/App/templates/pages/index.html' 
    def get_context_data(self, **kwargs): #puxar conteudo para html
        
        data = datetime.date.today()
        hora = (datetime.datetime.now())
        horaint = int(hora.strftime('%H'))
        print( '....................Hoje é Dia : ',data, '....................')
        print(hora)
        print('Hora:',horaint)
        if horaint <= 12:
            msg = "Bom Dia"
         
    
        if horaint >= 12:
            msg = "Boa Tarde" 
         
    
        if horaint >= 18:
            msg = "Boa Noite" 
        context = super().get_context_data(**kwargs)
        context["msg"] = msg
        context["data"] = data
        return context

class PrefeituraNew(GroupRequiredMixin, LoginRequiredMixin, CreateView,ListView):
    login_url=reverse_lazy('login')
    group_required = u'ADM'
    model=Prefeitura
    fields = ['nome',
              ]
    
    template_name = 'pages/prefeitura/prefeituraform.html'
    context_object_name = 'prefeituras'
    success_url =  reverse_lazy ('prefeitura_new')
    
    
   
    
    #definir um valor de usuario oculto para saber qual foi o user que fez a postagem
    def form_valid(self, form):
        
        form.instance.criadopor = self.request.user
        
        
        response = super().form_valid(form)
        messages.success(self.request, 'Prefeitura inserida com sucesso.')
        if response.status_code == 200:
            messages.error(self.request, 'erro')
        return response 
    
        
       
    
    
        
    
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        data = datetime.date.today()
        hora = (datetime.datetime.now())
        horaint = int(hora.strftime('%H'))
        print( '....................Hoje é Dia : ',data, '....................')
        print(hora)
        print('Hora:',horaint)
        if horaint <= 12:
            msg = "Bom Dia"
         
    
        if horaint >= 12:
            msg = "Boa Tarde" 
         
    
        if horaint >= 18:
            msg = "Boa Noite" 
        context = super().get_context_data(**kwargs)
        context["msg"] = msg
        context["data"] = data
        
        context['titulo'] = 'Criando Prefeitura'
        context['botao'] = 'Salvar'
        context['descri'] = 'Criação de Prefeitura.'
        
        return context    

class PrefeituraLista(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('login')
    model = Prefeitura
    template_name='pages/prefeitura/prefeituralista.html'
    
    # paginate_by = 2
    
    
    # #modo de pesquisar na lista por um colaborador
    # def get_queryset(self):
        
    #     txt_nome = self.request.GET.get('nome')
        
        
    #     if txt_nome:
        
    #         prefeitura = Prefeitura.objects.filter(nome__icontains=txt_nome)
            

    #     else:
    #         prefeitura = Prefeitura.objects.all()
            
            
    #     return prefeitura  
    
class PrefeituraUpdate(GroupRequiredMixin,LoginRequiredMixin, UpdateView,ListView):
    login_url = reverse_lazy('login')
    group_required = u'ADM','Gestor'
    model = Prefeitura
    fields = ['nome',
              ]
    template_name = 'pages/prefeitura/prefeituraform.html'
    success_url =  reverse_lazy ('prefeitura_new')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context['titulo'] = 'Editar Prefeitura'
        context['botao'] = 'Editar'
        context['descri'] = 'Edição de Dados.'
        
        return context
    
class PrefeituraDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Prefeitura
    
    template_name = 'pages/prefeitura/prefeituradelete.html'
    
    success_url = reverse_lazy('prefeitura_new')    
    
   
