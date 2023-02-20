from enum import unique
from django import forms

from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.urls import reverse_lazy

from App.views import Home







#registro
class UsuarioForm(UserCreationForm):
    email = forms.EmailField(max_length=100, label='Email')
    #grupo = forms.ModelMultipleChoiceField(queryset=Group.objects.filter(name__in=["ADM", 'Visitante']), required=True,widget=forms.CheckboxSelectMultiple)
    grupo = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=True,widget=forms.CheckboxSelectMultiple)

    class Meta:
        success_url =  reverse_lazy ('usuarioform.html')
        context_object_name = 'usuarios'
        model = User
        fields = ['username',
                  'email',
                  'password1',
                  'password2',
                  'is_active',
                  'grupo',
                  ]
        
 
  