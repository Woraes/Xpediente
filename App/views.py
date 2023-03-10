from io import BytesIO
import io
from django.contrib import messages
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import RequestContext
from django.views import View

from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView,FormView
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
from App.forms import FormSecretaria

from App.gerapdf import GeraPDF
from django import forms
from django.contrib.auth.views import LoginView

from usuarios.models import Perfil


#models
from .models import Historico, Prefeitura
from .models import Secretaria
from .models import Setor
from .models import Colaborador
from .models import Documento


#forms


#Home page
class Home(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = '/Xpediente/App/templates/pages/index.html' 
    def get_context_data(self, **kwargs): #puxar conteudo para html
        context = super().get_context_data(**kwargs)
        context['num_prefeitura'] = Prefeitura.objects.count()
        context['num_secretaria'] = Secretaria.objects.count()
        context['num_setor'] = Setor.objects.count()
        context['num_colaborador'] = Colaborador.objects.count()
        
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
    
    

#Classes Prefeitura
class PrefeituraNew(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url=reverse_lazy('login')
    group_required = u'ADM'
    model=Prefeitura
    #form = FormPrefeitura
    fields = ['nome',
              ]
    
    
    template_name = 'pages/prefeitura/prefeituraform.html'
    context_object_name = 'prefeituras'
    success_url =  reverse_lazy ('prefeitura_lista')
    
    
    # def FormPrefeitura(request):
    #     form = FormPrefeitura()
    #     contexto = {'form': form}
    #     return render(request, 'pages/prefeitura/prefeituraform.html', contexto)
    
    def form_valid(self, form):
        #definir um valor de usuario oculto para saber qual foi o user que fez a postagem
        form.instance.criadopor = self.request.user
        
        #validação de existente mais messagem flash
        # nome = form.cleaned_data.get('nome')
        # existing_prefeitura = Prefeitura.objects.filter(nome=nome).exists()
        # if existing_prefeitura:
        #     messages.info(self.request, "Existe uma Prefeitura Registrada com esse nome. Por favor escolha outro nome !!! Obrigado")
        #     return redirect("prefeitura_new")
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
    context_object_name = 'prefeituras'
    template_name='pages/prefeitura/prefeituralista.html'
    
    #pegando as informaçoes obtidas na class Home e passando para essa view
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(Home.as_view()(self.request).context_data)
        return context
    
   #modo de pesquisar na lista por um objeto
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

def requisicao_api(request):
        if request.method == 'POST':
            cep = request.POST['cep']
            response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
            if response.status_code == 200:
                dados = response.json()
                return render(request, 'cep.html', {"dados": dados})

        return redirect('secretaria_new')
    
class PrefeituraUpdate(GroupRequiredMixin,LoginRequiredMixin, UpdateView,ListView):
    login_url = reverse_lazy('login')
    group_required = u'ADM','Gestor'
    model = Prefeitura
    fields = ['nome',
              ]
    template_name = 'pages/prefeitura/prefeituraform.html'
    success_url =  reverse_lazy ('prefeitura_lista')
    
    #  #messagem flash de confirmaçã de edição
    def form_valid(self, form):
    #     form.instance.criadopor = self.request.user
    #     response = super().form_valid(form)
    #     messages.success(self.request, 'Prefeitura Editada com sucesso.')
    #     if response.status_code == 200:
    #         messages.error(self.request, 'erro')
    #     return response 
    
    #validação de existente mais messagem flash
        # nome = form.cleaned_data.get('nome')
        # existing_prefeitura = Prefeitura.objects.filter(nome=nome).exists()
        # if existing_prefeitura:
        #     messages.info(self.request, "Existe uma Prefeitura Registrada com esse nome. Por favor escolha outro nome !!! Obrigado")
        #     return redirect("prefeitura_lista")
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
    group_required = u'ADM'
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
class SecretariaNew(GroupRequiredMixin, LoginRequiredMixin, CreateView,FormView):
    login_url=reverse_lazy('login')
    group_required = u'ADM'
    model=Secretaria
    fields = [
            'nome',
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
    
    # form_class = FormSecretaria 
    template_name = 'pages/secretaria/secretariaform.html'
    context_object_name = 'secretarias'
    success_url =  reverse_lazy ('secretaria_lista')
    
    
    
    
    
    
    
    #Functions de Validar
    def form_valid(self, form):
        #instancia para pegar o criador
        form.instance.criadopor = self.request.user
         
        
    #      #validação de existente mais messagem flash
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
        #context.update(Home.as_view()(self.request).context_data)
        context['prefeituras'] = Prefeitura.objects.all()
        
        #Alterando o nome dos botoes no cadastro pois usamos o mesmo form
        context['titulo'] = 'Criando Secretária'
        context['botao'] = 'Criar'
        context['descri'] = 'Cadastro de Secretária.'
        
        return context
    
class SecretariaLista(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('login')
    model = Secretaria
    context_object_name = 'secretarias'
    template_name='pages/secretaria/secretarialista.html'
    
  
    #pegando as informaçoes obtidas na class Home e passando para essa view
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(Home.as_view()(self.request).context_data)
        return context
    
    # def get_queryset(self):
    #     status = self.request.GET.get('status') or self.request.GET.get('INATIVO')
    #     if status:
    #         if status == 'INATIVO':
    #             secretarias = Secretaria.objects.filter(status='inativo')
    #         else:
    #             secretarias = Secretaria.objects.filter(status='ativo')
    #     else:
    #         secretarias = Secretaria.objects.all()
    #     return secretarias

    
    
    #modo de pesquisar na lista por um objeto e dizer se esta ativo ou não e paginação
    paginate_by = 6
    def get_queryset(self):
        txt_nome = self.request.GET.get('nome')
        status = self.request.GET.get('status')
        if txt_nome:
             secretaria = Secretaria.objects.filter(nome__icontains=txt_nome)
             return secretaria 
        if status:  
            secretaria = Secretaria.objects.filter(status=status)
            return secretaria   
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
    success_url =  reverse_lazy ('secretaria_lista')
    
    
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
    
class SecretariaDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Secretaria
    
    template_name = 'pages/secretaria/secretariadelete.html'
    
    success_url = reverse_lazy('secretaria_lista')    
    
     #messagem flash de confirmação de exclusão
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.warning(self.request, 'Secretária Excluida com sucesso.')
        if response.status_code == 200:
            messages.error(self.request, 'erro')
        return response    
    
    #se existir uma prefeitura não apagar a secretaria
    # def form_valid(self, form):
    # # Check if a prefecture is registered
    #     if Prefeitura.objects.exists():
    #         messages.error(self.request, 'Não é possível excluir a secretária enquanto existir uma prefeitura registrada.')
    #         return super().form_invalid(form)

    #     response = super().form_valid(form)
    #     messages.warning(self.request, 'Secretária Excluida com sucesso.')
    #     return response

#Classes setor
class SetorNew(GroupRequiredMixin, LoginRequiredMixin, CreateView,ListView):
    login_url=reverse_lazy('login')
    group_required = u'ADM'
    model=Setor
    fields = ['nome',
              'prefeitura',
              'secretaria',
              'telefone',
              'status',
              'cep',
              'logradouro',
              'complemento',
              'bairro',
              'localidade',
              'uf',
              ]
    
    template_name = 'pages/setor/setorform.html'
    context_object_name = 'setores'
    success_url =  reverse_lazy ('setor_lista')    
    
    def form_valid(self, form):
        #definir um valor de usuario oculto para saber qual foi o user que fez a postagem
        form.instance.criadopor = self.request.user
        
        #validação de existente mais messagem flash
        nome = form.cleaned_data.get('nome')
        existing_prefeitura = Setor.objects.filter(nome=nome).exists()
        if existing_prefeitura:
            messages.info(self.request, "Existe um Setor Registrado com esse nome. Por favor escolha outro nome !!! Obrigado")
            return redirect("setor_new")
        response = super().form_valid(form)
        messages.success(self.request, "Setor adicionado com sucesso.")
        return response
    
     #alterando esses campos na view
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context.update(Home.as_view()(self.request).context_data)
        
        context['titulo'] = 'Criando Setor'
        context['botao'] = 'Criar'
        context['descri'] = 'Criação de setor.'
        
        return context
    
class SetorLista(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('login')
    model = Setor
    context_object_name = 'setores'
    template_name='pages/setor/setorlista.html'
    
    #pegando as informaçoes obtidas na class Home e passando para essa view
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(Home.as_view()(self.request).context_data)
        return context    
    
    #modo de pesquisar na lista por um objeto e dizer se esta ativo ou não
    paginate_by = 6
    def get_queryset(self):
        txt_nome = self.request.GET.get('nome')
        status = self.request.GET.get('status')
        if txt_nome:
             setor = Setor.objects.filter(nome__icontains=txt_nome)
             return setor 
        if status:  
            setor = Setor.objects.filter(status=status)
            return setor   
        else:
            setor = Setor.objects.all()
        return setor    
    
class SetorUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u'ADM','Gestor'
    model = Setor
    fields = fields = ['nome',
              'prefeitura',
              'secretaria',
              'telefone',
              'status',
              'cep',
              'logradouro',
              'complemento',
              'bairro',
              'localidade',
              'uf',
              ]
    template_name = 'pages/setor/setorform.html'
    success_url =  reverse_lazy ('setor_lista')   
    
    def form_valid(self, form):
        
        form.instance.criadopor = self.request.user
        
        
        response = super().form_valid(form)
        messages.success(self.request, 'Setor Editado com sucesso.')
        if response.status_code == 404:
            messages.error(self.request, 'erro')
        return response 
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context['titulo'] = 'Editar Setor'
        context['botao'] = 'Editar'
        context['descri'] = 'Edição de Dados.'
        
        return context     
    
class SetorDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Setor
    template_name = 'pages/setor/setordelete.html'
    success_url = reverse_lazy('setor_lista')        
    
     #se existir uma prefeitura não apagar a secretaria
    def form_valid(self, form):
    # Check if a prefecture is registered
        # if Secretaria.objects.exists():
        #     messages.error(self.request, 'Não é possível excluir o Setor, uma Secretária está vinculada.')
        #     return super().form_invalid(form)

        response = super().form_valid(form)
        messages.warning(self.request, 'Setor Excluido com sucesso.')
        return response  
    
#Classe colaborador    
class ColaboradorNew(GroupRequiredMixin, LoginRequiredMixin, CreateView):    
    login_url = reverse_lazy('login')
    group_required = u'ADM','Gestor'
    model = Colaborador
    fields = ['nome',
              #'nascimento',
              #'estadocivil',
              'matricula',
              'prefeitura',
              'secretaria',
              'setor',
            #   'rg',
              'cpf',
              #'pis',
              #'cns',
              #'ctps',
              #'ctpsserie',
              #'ctpsuf',
              'genero',
              'phone',
              'email',
              'foto',
              'status',
              'dataentrada',
              #'cep',
              #'logradouro',
              #'complemento',
              #'bairro',
              #'localidade',
              #'uf',
              ]
    template_name = 'pages/colaborador/colaboradorform.html'
    context_object_name = 'colaboradores'
    success_url =  reverse_lazy ('colaborador_lista')  
    
    def form_valid(self, form):
        #definir um valor de usuario oculto para saber qual foi o user que fez a postagem
        form.instance.criadopor = self.request.user
        
        #validação de existente mais messagem flash
        # nome = form.cleaned_data.get('nome')
        # matricula = form.cleaned_data.get('matricula')
        # existing_prefeitura = Colaborador.objects.filter(nome=nome).exists()
        # if existing_prefeitura:
        #     messages.info(self.request, "Existe um Colaborador Registrado com esse nome. Por favor escolha outro nome !!! Obrigado")
        #     return redirect("colaborador_new")
        # existing_matricula = Colaborador.objects.filter(matricula=matricula).exists()
        # if existing_matricula:
        #     messages.info(self.request, "Existe uma Matrícula Registrada. Por favor escolha outra!!! Obrigado")
        #     return redirect("colaborador_new")
        # else:
        response = super().form_valid(form)
        messages.success(self.request, "Colaborador adicionado com sucesso.")
        return response
    
     #alterando esses campos na view
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(Home.as_view()(self.request).context_data)
        context['titulo'] = 'Criando Colaborador'
        context['botao'] = 'Criar'
        context['descri'] = 'Criação de colaborador.'
        
        return context
    
class ColaboradorLista(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('login')
    model = Colaborador
    context_object_name = 'colaboradores'
    template_name='pages/colaborador/colaboradorlista.html'
    
    #pegando as informaçoes obtidas na class Home e passando para essa view
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(Home.as_view()(self.request).context_data)
        return context    
    
    #modo de pesquisar na lista por um objeto e dizer se esta ativo ou não
    paginate_by = 6
    def get_queryset(self):
        txt_nome = self.request.GET.get('nome')
        status = self.request.GET.get('status')
        if txt_nome:
             setor = Colaborador.objects.filter(nome__icontains=txt_nome)
             return setor 
        if status:  
            setor = Colaborador.objects.filter(status=status)
            return setor   
        else:
            setor = Colaborador.objects.all()
        return setor        
    
class ColaboradorUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u'ADM','Gestor'
    model = Colaborador
    fields = ['nome',
              #'nascimento',
              #'estadocivil',
              'matricula',
              'prefeitura',
              'secretaria',
              'setor',
            #   'rg',
              'cpf',
              #'pis',
              #'cns',
              #'ctps',
              #'ctpsserie',
              #'ctpsuf',
              'genero',
              'phone',
              'email',
              'foto',
              'status',
              'dataentrada',
              #'cep',
              #'logradouro',
              #'complemento',
              #'bairro',
              #'localidade',
              #'uf',
              ]
    template_name = 'pages/colaborador/colaboradorform.html'
    success_url =  reverse_lazy ('colaborador_lista')   
    
    def form_valid(self, form):
        
        form.instance.criadopor = self.request.user
        
        
        response = super().form_valid(form)
        messages.success(self.request, 'Colaborador Editado com sucesso.')
        if response.status_code == 404:
            messages.error(self.request, 'erro')
        return response 
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context['titulo'] = 'Editar Colaborador'
        context['botao'] = 'Editar'
        context['descri'] = 'Edição de Dados.'
        
        return context         
    
class ColaboradorDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = Colaborador
    template_name = 'pages/colaborador/colaboradordelete.html'
    success_url = reverse_lazy('colaborador_lista')        
    
     #se existir uma prefeitura não apagar a secretaria
    def form_valid(self, form):
    # Check if a prefecture is registered
        if Secretaria.objects.exists():
            messages.error(self.request, 'Não é possível excluir o Colaborador, uma Secretária está vinculada.')
            return super().form_invalid(form)

        response = super().form_valid(form)
        messages.warning(self.request, 'colaborador Excluido com sucesso.')
        return response      


#Documento
class DocumentoNew(GroupRequiredMixin, LoginRequiredMixin, CreateView,FormView):    
    login_url = reverse_lazy('login')
    group_required = u'ADM','UBS LEANDRO','UBS MAZOMBA'
    model = Documento
    fields = ['nome',
              'tipo',
              'numeracao',
              'ano',
              'assunto',
              #'datainicial',
              #'prefeitura',
              #'secretaria',
              #'setor',
              #'status',
              'anexo',
              ]
    template_name = 'pages/documento/documentoform.html'
    context_object_name = 'documentos'
    success_url =  reverse_lazy ('documento_lista')  
    
   #get_initial é um método que retorna um dicionário com os valores iniciais para os campos do formulário. Nesse caso, ele está buscando as informações do perfil do usuário que está acessando a página.
    def get_initial(self):
        initial = super().get_initial()
        perfil = self.request.user.perfil
        initial['prefeitura'] = perfil.prefeitura_id
        initial['secretaria'] = perfil.secretaria_id
        initial['setor'] = perfil.setor_id
        return initial
    
   #form_valid é um método que é chamado após a validação do formulário, e é responsável por salvar os dados no banco de dados. Nesse caso, ele está definindo alguns valores nos campos do objeto do modelo que serão salvos.
    def form_valid(self, form):
        data = datetime.date.today()
        form.instance.criadopor = self.request.user
        form.instance.datainicial = data
        form.instance.status = 'registrado'
        form.instance.origem = self.request.user
        form.instance.destino = self.request.user
        form.instance.prefeitura = self.request.user.perfil.prefeitura
        form.instance.secretaria = self.request.user.perfil.secretaria
        form.instance.setor = self.request.user.perfil.setor
        response = super().form_valid(form)
        messages.success(self.request, "Documento adicionado com sucesso.")
        return response
    
     #alterando esses campos na view
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        #context.update(Home.as_view()(self.request).context_data)
        context['titulo'] = 'Registrando Documento'
        context['botao'] = 'Criar'
        context['descri'] = 'Registro de Documento.'
        
        return context    
    
#Documentos Criados
class DocumentoLista(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('login')
    model = Documento
    context_object_name = 'documentos'
    template_name='pages/documento/documentolista.html'
    
     
    
     #modo de pesquisar na lista por um objeto e dizer se esta ativo ou não
    paginate_by = 0
    def get_queryset(self):
        txt_numeracao = self.request.GET.get('nome')
        status = self.request.GET.get('status')
        if txt_numeracao:
             documento =Documento.objects.filter(nome__icontains=txt_numeracao)
             return documento 
        if status:  
            documento = Documento.objects.filter(status=status)
            return documento   
        else:
            documento = Documento.objects.all()
        return documento        
     
    #pegando as informaçoes obtidas na class Home e passando para essa view
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(Home.as_view()(self.request).context_data)
        
        context['titulo'] = 'Registrando Documento'
        context['botao'] = 'Criar'
        context['descri'] = 'Registro de Documento.'
        return context   
    
    
class DocumentoEnviar(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u'ADM','UBS LEANDRO','UBS MAZOMBA'
    model = Documento
    fields = [#'nome',
              #'tipo',
              #'numeracao',
              #'ano',
              #'assunto',
              #'datainicial',
              #'data_envio',
              #'prefeitura',
              'secretaria',
              'setor',
              #'status',
              'anexo',
              ]
    template_name = 'pages/documento/documentos_mover.html'
    success_url =  reverse_lazy ('documento_lista')   
    
    #Neste form_validmétodo modificado, primeiro salvamos a Documentoinstância atualizada e, em seguida, obtemos a Setorinstância selecionada do setorcampo do formulário usando a setor_idvariável. Em seguida, criamos o novo Historicoobjeto com as instâncias corretas Documentoe Setorusando o create()método do Historicogerenciador de modelos. Isso deve criar o Historicoobjeto com a Setorinstância correta e evitar o ValueError.
    def form_valid(self, form):
        data = datetime.date.today()
        form.instance.criadopor = self.request.user
        form.instance.status = 'enviado'
        form.instance.data_envio = data
        
        documento = form.save()
        
        
        setor_id = self.request.POST.get('setor')
        setor = Setor.objects.get(id=setor_id)
        
        Historico.objects.create(documento=documento,setor=setor, data_entrada=data, data_saida=data, criadopor=self.request.user)
            

      
        messages.success(self.request, 'Documento enviado com sucesso.')
        return super().form_valid(form)

    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context['titulo'] = 'Envio de documento '
        context['botao'] = 'Enviar'
        context['descri'] = 'Dados do Documento'
        
        return context       
    
    
class DocumentoRecebido(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u'ADM','UBS LEANDRO','UBS MAZOMBA'
    model = Documento
    fields = [#'nome',
              #'tipo',
              #'numeracao',
              #'ano',
              #'assunto',
              #'datainicial',
              #'data_recebimento',
              #'prefeitura',
              #'secretaria',
              #'setor',
              'status',
              #'anexo',
              ]
    template_name = 'pages/documento/documentos_receber.html'
    success_url =  reverse_lazy ('documentosreceber_lista')   
    
    #Neste form_validmétodo modificado, primeiro salvamos a Documentoinstância atualizada e, em seguida, obtemos a Setorinstância selecionada do setorcampo do formulário usando a setor_idvariável. Em seguida, criamos o novo Historicoobjeto com as instâncias corretas Documentoe Setorusando o create()método do Historicogerenciador de modelos. Isso deve criar o Historicoobjeto com a Setorinstância correta e evitar o ValueError.
    def form_valid(self, form):
        data = datetime.date.today()
        form.instance.criadopor = self.request.user
        form.instance.status = 'recebido'
        form.instance.data_recebimento = data
        
        
        documento = form.save()
        
        
        setor = self.request.user.perfil.setor
        
        Historico.objects.create(documento=documento,setor=setor, data_entrada=data, data_saida=data, criadopor=self.request.user)
            

      
        messages.success(self.request, 'Documento Recebido com sucesso.')
        return super().form_valid(form)

  
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context['titulo'] = 'Envio de documento '
        context['botao'] = 'Receber'
        context['descri'] = 'Dados do Documento'
        
        return context      
 
 
class DocumentoReceberLista(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('login')
    model = Documento
    context_object_name = 'documentos'
    template_name='pages/documento/documentoreceberlista.html'
    
     
    
     #modo de pesquisar na lista por um objeto e dizer se esta ativo ou não
    paginate_by = 0
    def get_queryset(self):
        txt_numeracao = self.request.GET.get('nome')
        status = self.request.GET.get('status')
        if txt_numeracao:
             documento =Documento.objects.filter(nome__icontains=txt_numeracao)
             return documento 
        if status:  
            documento = Documento.objects.filter(status=status)
            return documento   
        else:
            documento = Documento.objects.all()
        return documento        
     
    #pegando as informaçoes obtidas na class Home e passando para essa view
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(Home.as_view()(self.request).context_data)
        
        context['titulo'] = 'Registrando Documento'
        context['botao'] = 'Criar'
        context['descri'] = 'Registro de Documento.'
        return context    
 
 
 
    
class DocumentoView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u'ADM','UBS LEANDRO','UBS MAZOMBA'
    model = Documento
    fields = [#'nome',
              #'tipo',
              #'numeracao',
              #'ano',
              #'assunto',
              #'datainicial',
              #'data_envio',
              #'prefeitura',
              'secretaria',
              'setor',
              #'status',
              'anexo',
              ]
    template_name='pages/documento/documentoview.html'
    success_url =  reverse_lazy ('documento_lista')   
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historicos'] = self.object.historico_set.all()
        return context
    

     
       