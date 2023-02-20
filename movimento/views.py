from django.shortcuts import render, redirect
from App.models import Documento


from movimento.form import FormDocumento

# Create your views here.


# def criar_documento(request):
#     if request.method == 'POST':
#         form = FormDocumento(request.POST)
#         if form.is_valid():
#             documento = form.save(commit=False)
#             documento.status = 'enviado'
#             documento.save()
#             return redirect('documento_view', id=documento.id)
#     else:
#         form = FormDocumento()
#     return render(request, 'documentoform.html', {'form': form})

# def visualizar_documento(request, id):
#     documento = Documento.objects.get(id=id)
#     return render(request, 'documentoview.html', {'documento': documento})


# def confirmar_recebimento(request, id):
#     documento = Documento.objects.get(id=id)
#     documento.status = 'recebido'
#     documento.save()
#     return redirect('documento_view', id=documento.id)



# def doc_list(request):
#     documento = Documento.objects.all()
    
#     return render(request,  'documentolista.html', {'documento': documento})