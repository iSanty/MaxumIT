from django.shortcuts import render

from .models import PedidoParaMail

# Create your views here.


def index_saladillo(request):
    return render(request, 'saladillo/index_saladillo.html')


def monitor(request):
    
    pedidos = PedidoParaMail.objects.all()
    
    pedido_primer_mail = pedidos.filter(mail1_enviado=1)
    
    
    return render(request, 'saladillo/monitor.html')