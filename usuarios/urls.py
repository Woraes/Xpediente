from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import UsuarioNew,UsuarioLista,UsuarioUpdate,UsuarioDelete,PerfilUpdate
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        extra_context={'titulo': 'Autenticação'}
        ),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('alterar-minha-senha/', auth_views.PasswordChangeView.as_view(
        template_name='alterasenhaform.html',
        extra_context={'titulo': 'Alterar senha atual'},
        success_url=reverse_lazy('home')
        ), name="alterasenha"),
    
    #Usuario
    path('usuarionew/', UsuarioNew.as_view(), name='usuario_new'),
    path('usuariolista/', UsuarioLista.as_view(), name='usuario_lista'),
    path('usuario_update/<int:pk>', UsuarioUpdate.as_view(), name='usuario_update'),
    path('usuario_delete/<int:pk>', UsuarioDelete.as_view(), name='usuario_delete'),
    
    
    #Perfil
    path('perfilupdate/', PerfilUpdate.as_view(), name='perfil_update'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)