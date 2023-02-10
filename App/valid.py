



from .views import PrefeituraNew



def unique_prefeitura(value):
           if PrefeituraNew.objects.filter(nome=value).exists():
            raise PrefeituraNew('Prefeitura já existe.')   