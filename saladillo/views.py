from django.shortcuts import render

from .models import PedidoParaMail, MaestroCliente, PrimeraInstancia
from stg.models import pedidos, clientes_emails
from datetime import datetime, date
from .forms import FormActualizarPedidos
from .funciones import mail_primera_instancia

formato_fecha = "%d/%m/%Y %H:%M:%S"
formato_fecha2 = "%d/%m/%Y"
hoy = datetime.today()
dia = hoy.day
mes = hoy.month
anio = hoy.year
fecha_hoy = str(dia) + '/' + str(mes) + '/' + str(anio)
fecha_hoy_f = datetime.strptime(fecha_hoy, formato_fecha2)
# Create your views here.


def index_saladillo(request):
    
    if request.method == 'POST':
        form = FormActualizarPedidos(request.POST)
        form2 = FormActualizarPedidos(request.POST)
        if form.is_valid():
            
            if 'btn_carga' in request.POST:
            
                un_dia = form.cleaned_data
                
                pedidos_nuevos = pedidos.objects.filter(fecha=un_dia['fecha'])
                contador = 0
                
                for valor in pedidos_nuevos:
                    listar_pedidos = PedidoParaMail.objects.filter(nro_pedido=valor.numero)
                    
                    if not listar_pedidos:
                        nuevo_pedido = PedidoParaMail(
                            codigo_cliente = valor.codigo_cliente,
                            nro_pedido = valor.numero,
                            mail1_enviado = 0,
                            mail2_enviado = 0,
                            mail3_enviado = 0,
                            cantidad = 0,
                            importe_total = valor.importe_total_comprobante,
                            orden_de_compra = valor.ordendecompra,
                            fecha_creacion = fecha_hoy_f
                        )
                        
                        nombre_cliente = MaestroCliente.objects.filter(codigo=valor.codigo_cliente)
                        
                        if not nombre_cliente:
                            nuevo_pedido.cliente = 'S/D ' + str(valor.codigo_cliente)
                            
                        else:
                            nombre_cliente = MaestroCliente.objects.get(codigo=valor.codigo_cliente)
                            nuevo_pedido.cliente = nombre_cliente.nombre
                            
                            buscar_mail = clientes_emails.objects.filter(nombre=nombre_cliente.nombre)
                            if buscar_mail:
                                buscar_mail = clientes_emails.objects.get(nombre=nombre_cliente.nombre)
                                if buscar_mail.email_1:
                                    nuevo_pedido.mail = buscar_mail.email_1
                                else:
                                    if buscar_mail.email_2:
                                        nuevo_pedido.mail = buscar_mail.email_2
                                    else:
                                        
                                        if buscar_mail.email_3:
                                            nuevo_pedido.mail = buscar_mail.email_3
                                        else:
                                            nuevo_pedido.mail = 'Sin Datos'
                            
                            
                        
                        
                        nuevo_pedido.save()
                        contador += 1
                    
                        
                cantidad_pedidos = len(pedidos_nuevos)
                
                if contador:
                    pedidos_cargados = PedidoParaMail.objects.filter(fecha_creacion=fecha_hoy_f)
                else:
                    pedidos_cargados = ''
                
                msj_carga = 'Conexión exitosa. Se han leido un total de: ' + str(cantidad_pedidos) + ' lineas de la fecha: ' + str(un_dia['fecha']) + ' y se han generado un total de: ' + str(contador) + ' pedidos nuevos.'
                return render(request, 'saladillo/index_saladillo.html', {'msj_carga':msj_carga, 'pedidos':pedidos_cargados, 'form':form, 'form2':form2})
            

            
            elif 'btn_enviar_mail' in request.POST:
                pendientes_totales = PedidoParaMail.objects.filter(mail1_enviado=False)
                total_sin_datos = 0
                total_enviados = 0
                
                if pendientes_totales:
                    for valor in pendientes_totales:
                        if valor.mail == 'Sin Datos':
                            total_sin_datos += 1
                            
                        else:
                            
                            mail_primera_instancia(cliente=valor.cliente, importe_total=valor.importe_total, mail=valor.mail, orden_de_compra=valor.orden_de_compra, nro_pedido=valor.nro_pedido)
                            total_enviados += 1
                            valor.mail1_enviado = True
                            valor.save()
                    
                    return render(request, 'saladillo/index_saladillo.html', {'msj_enviados':total_enviados,
                                                                              'form':form,
                                                                              'form2':form2,
                                                                              'msj_no_enviado':total_sin_datos})
                else:
                    
                    msj_error = 'No hay pendientes de enviar. Chequee seccion "Sin Datos"'
                    return render(request, 'saladillo/index_saladillo.html', {'msj_enviados':total_enviados, 
                                                                              'form':form, 
                                                                              'form2':form2, 
                                                                              'msj_no_enviado':total_sin_datos,
                                                                              'msj_error':msj_error})
        
        
        else:
            msj_error = 'Formulario inválido.'
            return render(request, 'saladillo/index_saladillo.html', {'msj_error':msj_error, 'form':form, 'form2':form2})
    else:
    
        form2 = FormActualizarPedidos(initial={
            'fecha':fecha_hoy})
        
        form = FormActualizarPedidos(initial={
            'fecha':fecha_hoy})
        pendientes_mail = PedidoParaMail.objects.filter(mail1_enviado=False)
        total_pend_mail_1 = len(pendientes_mail)
        msj_inicio = 'Para accionar utilice los siguientes botones: '
        return render(request, 'saladillo/index_saladillo.html', {'form':form,'msj_inicio':msj_inicio, 'form2':form2, 'pendientes':total_pend_mail_1})






def monitor(request):
    
    enviados = PrimeraInstancia.objects.all()
    
    pendientes = PedidoParaMail.objects.filter(mail1_enviado=False)
    
    
    return render(request, 'saladillo/monitor.html',{'enviados':len(enviados), 'pendientes':len(pendientes)})