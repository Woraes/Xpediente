from io import BytesIO
import io
from django.contrib import messages
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from braces.views import GroupRequiredMixin
from django.core.paginator import Paginator
import datetime
import requests

from django.template.loader import get_template
from xhtml2pdf import pisa
from reportlab.pdfgen import canvas



#validação de erros
from django.core.exceptions import ValidationError
from App.gerapdf import GeraPDF

from django import forms

#models
from .models import Prefeitura
from .models import Secretaria

# Create your views here.



class Home(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = '/Xpediente/App/templates/pages/index.html' 
    def get_context_data(self, **kwargs): #puxar conteudo para html
        context = super().get_context_data(**kwargs)
        context['num_prefeitura'] = Prefeitura.objects.count()
        context['num_secretaria'] = Secretaria.objects.count()
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
        context["msg"] = msg
        context["data"] = data    
        return context

class PrefeituraNew(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url=reverse_lazy('login')
    group_required = u'ADM'
    model=Prefeitura
    fields = ['nome',
              ]
    
    template_name = 'pages/prefeitura/prefeituraform.html'
    context_object_name = 'prefeituras'
    success_url =  reverse_lazy ('prefeitura_new')
    
    
     
    
    def form_valid(self, form):
        #definir um valor de usuario oculto para saber qual foi o user que fez a postagem
        form.instance.criadopor = self.request.user
        
        #validação de existente mais messagem flash
        nome = form.cleaned_data.get('nome')
        existing_prefeitura = Prefeitura.objects.filter(nome=nome).exists()
        if existing_prefeitura:
            messages.info(self.request, "Existe uma Prefeitura Registrada com esse nome. Por favor escolha outro nome !!! Obrigado")
            return redirect("prefeitura_new")
        response = super().form_valid(form)
        messages.success(self.request, "Prefeitura adicionada com sucesso.")
        return response
    
    #alterando esses campos na view
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context.update(Home.as_view()(self.request).context_data)
        
        context['titulo'] = 'Criando Prefeitura'
        context['botao'] = 'Criar'
        context['descri'] = 'Criação de Prefeitura.'
        
        return context
    

class PrefeituraLista(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('login')
    model = Prefeitura
    context_object_name = 'prefeituralist'
    template_name='pages/prefeitura/prefeituralista.html'
    
    #pegando as informaçoes obtidas na class Home e passando para essa view
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(Home.as_view()(self.request).context_data)
        return context
    
   #modo de pesquisar na lista por um colaborador
    paginate_by = 6
    def get_queryset(self):
        txt_nome = self.request.GET.get('nome')
        if txt_nome:
            prefeitura = Prefeitura.objects.filter(nome__icontains=txt_nome)
        else:
            prefeitura = Prefeitura.objects.all()
        return prefeitura 
    
   
     
        
def prefeitura_view(request):
    # Crie o objeto HttpResponse com o cabeçalho de PDF apropriado.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'
        buffer = io.BytesIO()
    # Crie o objeto PDF, usando o objeto response como seu "arquivo".
        #p = canvas.Canvas(response),
        p = canvas.Canvas(buffer)
            

    # Desenhe coisas no PDF. Aqui é onde a geração do PDF acontece.
    # Veja a documentação do ReportLab para a lista completa de
    # funcionalidades.
        
        p.setFont('Helvetica', 32)
        p.setFillColor('gray')       
        p.drawCentredString(300, 770, "Ficha")
        
        p.setFont('Helvetica', 25)
        p.setFillColor('gray') 
        p.drawCentredString(200, 770, "Relatórios")
        # p.line('x1', 'y1', 'x2')
        # p.lines(linelist)
        # p.grid(xlist, ylist) 
        # p.bezier()
        # p.arc(x1,y1,x2,y2) 
        # p.rect(x, y, width, height, stroke=1, fill=0) 
        # p.ellipse(x1,y1, x2,y2, stroke=1, fill=0)
        # p.wedge(x1,y1, x2,y2, startAng, extent, stroke=1, fill=0) 
        # p.circle(x_cen, y_cen, r, stroke=1, fill=0)
        # p.roundRect(x, y, width, height, radius, stroke=1, fill=0)

    # Feche o objeto PDF, e está feito.
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='file.pdf')
    
    

    
    
class PrefeituraUpdate(GroupRequiredMixin,LoginRequiredMixin, UpdateView,ListView):
    login_url = reverse_lazy('login')
    group_required = u'ADM','Gestor'
    model = Prefeitura
    fields = ['nome',
              ]
    template_name = 'pages/prefeitura/prefeituraform.html'
    success_url =  reverse_lazy ('prefeitura_new')
    
    #  #messagem flash de confirmaçã de edição
    def form_valid(self, form):
    #     form.instance.criadopor = self.request.user
    #     response = super().form_valid(form)
    #     messages.success(self.request, 'Prefeitura Editada com sucesso.')
    #     if response.status_code == 200:
    #         messages.error(self.request, 'erro')
    #     return response 
    
    #validação de existente mais messagem flash
        nome = form.cleaned_data.get('nome')
        existing_prefeitura = Prefeitura.objects.filter(nome=nome).exists()
        if existing_prefeitura:
            messages.info(self.request, "Existe uma Prefeitura Registrada com esse nome. Por favor escolha outro nome !!! Obrigado")
            return redirect("prefeitura_lista")
        response = super().form_valid(form)
        messages.success(self.request, "Prefeitura Editada com sucesso.")
        return response
    
    #alterando esses campos na view
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
    
    success_url = reverse_lazy('prefeitura_lista')    
    
    #messagem flash de confirmação de exclusão
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.warning(self.request, 'Prefeitura Excluida com sucesso.')
        if response.status_code == 200:
            messages.error(self.request, 'erro')
        return response 
    
class GerarPdfView(GroupRequiredMixin,LoginRequiredMixin, View, GeraPDF):
    login_url = reverse_lazy('login')
    group_required = u'ADM'
    model = Prefeitura
    
    def get(self, request, *args, **kwargs):
       
       try:
            #Criando objeto que vai retornar
            template = get_template('pages/prefeitura/prefeiturapdf.html')
            context = {'title': 'Relatório',
                       'nome': 'Prefeitura'
                       }
           
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #aqui para salvar no pc
            response['Content-Disposition'] = 'attachment; filename="file.pdf"'
            
            #Criando pdf
            pisaStatus = pisa.CreatePDF(
                html, dest=response)
            
        

            return response
        
       except:
            pass
       return HttpResponseRedirect(reverse_lazy('prefeitura_new'))



#Classes secretaria
class SecretariaNew(GroupRequiredMixin, LoginRequiredMixin, CreateView,ListView):
    login_url=reverse_lazy('login')
    group_required = u'ADM'
    model=Secretaria
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
    
    template_name = 'pages/secretaria/secretariaform.html'
    context_object_name = 'secretarias'
    success_url =  reverse_lazy ('secretaria_new')
    
    #Functions de Validar
    def form_valid(self, form):
        #instancia para pegar o criador
        form.instance.criadopor = self.request.user
        
         #validação de existente mais messagem flash
        nome = form.cleaned_data.get('nome')
        sigla = form.cleaned_data.get('sigla')

        existing_secretaria = Secretaria.objects.filter(nome=nome).exists()
        if existing_secretaria:
            messages.info(self.request, "Existe uma Secretaria Registrada com esse nome. Por favor escolha outro nome !!! Obrigado")
            return redirect("secretaria_new")
       
        
        existing_secretariasigla = Secretaria.objects.filter(sigla=sigla).exists()
        if existing_secretariasigla:
            messages.info(self.request, "Existe uma SIGLA para Secretaria Registrada com esse nome. Por favor escolha outro nome !!! Obrigado")
            return redirect("secretaria_new")
        
        else:
            response = super().form_valid(form)
            messages.success(self.request, "Secretaria adicionada com sucesso.")
            return response
        
        
        
        # #Flash Menssage
        # response = super().form_valid(form)
        # messages.success(self.request, 'Secretária inserida com sucesso.')
        # if response.status_code == 500:
        #     messages.error(self.request, 'erro')
        # return response 
    
    #Pegar o conteudo    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        #pegando o conteudo desse template
        context.update(Home.as_view()(self.request).context_data)
        
        
        #Alterando o nome dos botoes no cadastro pois usamos o mesmo form
        context['titulo'] = 'Criando Secretária'
        context['botao'] = 'Criar'
        context['descri'] = 'Cadastro de Secretária.'
        
        return context
    
            
class SecretariaLista(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('login')
    model = Secretaria
    template_name='pages/secretaria/secretarialista.html'
    
    #pegando as informaçoes obtidas na class Home e passando para essa view
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(Home.as_view()(self.request).context_data)
        return context
    
    #modo de pesquisar na lista por um colaborador
    paginate_by = 6
    def get_queryset(self):
        txt_nome = self.request.GET.get('nome')
        if txt_nome:
            secretaria = Secretaria.objects.filter(nome__icontains=txt_nome)
        else:
            secretaria = Secretaria.objects.all()
        return secretaria      
    
class SecretariaUpdate(GroupRequiredMixin,LoginRequiredMixin, UpdateView,ListView):
    login_url = reverse_lazy('login')
    group_required = u'ADM','Gestor'
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
    template_name = 'pages/secretaria/secretariaform.html'
    success_url =  reverse_lazy ('secretaria_new')
    
    
    def form_valid(self, form):
        
        form.instance.criadopor = self.request.user
        
        
        response = super().form_valid(form)
        messages.success(self.request, 'Scretária Editada com sucesso.')
        if response.status_code == 404:
            messages.error(self.request, 'erro')
        return response 
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context['titulo'] = 'Editar Secretária'
        context['botao'] = 'Editar'
        context['descri'] = 'Edição de Dados.'
        
        return context    