from django.shortcuts import render

from .models import PedidoParaMail
from stg.models import pedidos
from datetime import datetime, date

# Create your views here.


def index_saladillo(request):
    
    
    if request.method == 'POST':
        
        if 'btn_carga' in request.POST:
        
            un_dia = date.fromisoformat('2023-03-18')
            
            pedidos_nuevos = pedidos.objects.filter(fecha=un_dia)
            contador = 0
            
            for valor in pedidos_nuevos:
                listar_pedidos = PedidoParaMail.objects.filter(nro_pedido=valor.numero)
                
                if not listar_pedidos:
                    nuevo_pedido = PedidoParaMail(
                        cliente = 'crear tabla maestro clientes',
                        nro_pedido = valor.numero,
                        mail = 'crear tabla maestro clientes',
                        mail1_enviado = 0,
                        mail2_enviado = 0,
                        mail3_enviado = 0,
                        cantidad = 0,
                        importe_total = valor.importe_total_comprobante,
                        orden_de_compra = valor.ordendecompra,
                        fecha_creacion = date.today()
                    )
                    nuevo_pedido.save()
                    contador += 1
                
                    
            cantidad_pedidos = len(pedidos_nuevos)

            pedidos_cargados = PedidoParaMail.objects.filter(fecha_creacion=date.today())
            msj_carga = 'Base Actualizada correctamente. Se han leido un total de: ' + str(cantidad_pedidos) + ' pedidos de la fecha: ' + str(un_dia) + ' y se han generado un total de: ' + str(contador) + ' pedidos nuevos.'
            return render(request, 'saladillo/index_saladillo.html', {'msj_carga':msj_carga, 'pedidos':pedidos_cargados})
        

        
        elif 'btn_enviar_mail' in request.POST:
            msj_enviados = 'Mails Enviados'
            return render(request, 'saladillo/index_saladillo.html', {'msj_enviados':msj_enviados})

        
    else:
    
    
    
    
        msj_inicio = 'Para accionar utilice los siguientes botones: '
        return render(request, 'saladillo/index_saladillo.html', {'msj_inicio':msj_inicio})






def monitor(request):
    
    pedidos = PedidoParaMail.objects.all()
    
    pedido_primer_mail = pedidos.filter(mail1_enviado=1)
    
    
    return render(request, 'saladillo/monitor.html')