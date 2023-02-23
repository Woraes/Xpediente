from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.views.generic.list import ListView
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.shortcuts import get_object_or_404

from App.views import Home

from .form import UsuarioForm
from .models import  User,Perfil


# Create your views here.
class UsuarioNew(GroupRequiredMixin ,LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = u'ADM'
    template_name = 'usuarioform.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('usuario_new')

    
    def form_valid(self, form):
        form.instance.criadopor = self.request.user
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        grupos = form.cleaned_data['grupo']
        self.object.groups.set(grupos)
        messages.success(self.request, "Usuário criado com sucesso.")
        
        
        #Criando um perfil para retornar para usuario
        Perfil.objects.create(usuario=self.object)
        return super().form_valid(form)
    
     
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        #puxando de home os {{}}
        #context.update(Home.as_view()(self.request).context_data)
        #alterando esses campos na view
        context['titulo'] = 'Criando Usuário'
        context['botao'] = 'Criar'
        context['descri'] = 'Criação de Usuário.'
        return context
    
    
    
class UsuarioLista(LoginRequiredMixin,ListView):
    login_url = reverse_lazy('login')
    model = User
    context_object_name = 'usuarios'
    template_name='usuariolista.html'
    
    #pegando as informaçoes obtidas na class Home e passando para essa view
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(Home.as_view()(self.request).context_data)
        return context    
    
    #modo de pesquisar na lista por um objeto e dizer se esta ativo ou não
    paginate_by = 5
    def get_queryset(self):
        txt_nome = self.request.GET.get('username')
        status = self.request.GET.get('is_active')
        if txt_nome:
             setor = User.objects.filter(username__icontains=txt_nome)
             return setor 
        if status:  
            setor = User.objects.filter(is_active=status)
            print (status)
            return setor   
        else:
            setor = User.objects.all()
        return setor        
    
    
class UsuarioUpdate(GroupRequiredMixin,LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = u'ADM','Gestor'
    form_class = UsuarioForm
    queryset = User.objects.filter(is_active=True)
    template_name = 'usuarioform.html'
    success_url = reverse_lazy('usuario_lista')
    
    
    def get_queryset(self):
        return self.queryset
    
    def form_valid(self, form):
        form.instance.criadopor = self.request.user
        
        response = super().form_valid(form)
        messages.success(self.request, 'Usuário Editada com sucesso.')
        if response.status_code == 404:
            messages.error(self.request, 'erro')
        return response 
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # obtém o usuário sendo editado
        usuario = self.object
        # obtém os grupos anteriores do usuário
        grupos_anteriores = list(usuario.groups.all().values_list('name', flat=True))
    
        # adiciona os grupos anteriores ao contexto
        context['grupos_anteriores'] = grupos_anteriores
        
        context['titulo'] = 'Editar Usuário'
        context['botao'] = 'Editar'
        context['descri'] = 'Edição de Dados.'
        
        return context    
    
class UsuarioDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):    
    login_url = reverse_lazy('login')
    group_required = u'Administrador'
    model = User
    
    
    template_name = 'usuariodelete.html'
    
    success_url = reverse_lazy('usuario_lista')    
    
     #messagem flash de confirmação de exclusão
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.warning(self.request, 'Usuário Excluida com sucesso.')
        if response.status_code == 200:
            messages.error(self.request, 'erro')
        return response  
    
    
    #Perfil
class PerfilUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    
    model = Perfil
    fields = ['nome',
                  'cpf',
                  'matricula',
                  'telefone',
                  'email',
                  'foto',
                  #'cep',
                  'prefeitura',
                  'secretaria',
                  'setor',
                  ]
    template_name = 'perfil/perfilform.html'
    success_url = reverse_lazy('home')
     
    def form_valid(self, form):   
        messages.success(self.request, 'Perfil Atualizado com sucesso.')
        return super().form_valid(form)
    #def oara pegar o objeto
    def get_object(self, queryset=None):
        self.object = get_object_or_404(Perfil, usuario=self.request.user)
        return self.object
        
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(Home.as_view()(self.request).context_data)
        context['titulo'] = 'Editar Perfil'
        context['botao'] = 'Salvar'
        context['descri'] = 'Edição de Dados.'
        
        return context    