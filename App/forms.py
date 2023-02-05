




from django.contrib.auth.models import User
from django import forms

from App import models




class PrefeituraForm(forms.form):
        nome = forms.CharField(widget=forms.DateInput)
        widget =forms.RadioSelect()
        criadopor = models.ForeignKey(User, on_delete=models.PROTECT)
        def __str__(self):
            return '{} - Criado por:({}) '.format(self.nome, self.criadopor)  