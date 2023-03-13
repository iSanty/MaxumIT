from django.shortcuts import render

from .models import stg_pedidos
# Create your views here.



def leer_saladillo(request):
    
    pedidos = stg_pedidos.objects.all()
    
    print(pedidos)

    return render(request, 'saladillo/index_saladillo.html')