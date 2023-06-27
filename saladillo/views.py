from django.shortcuts import render

from .models import PedidoParaMail, MaestroCliente, PrimeraInstancia, MailReceptor, CuerpoMail, HojaRuta
from stg.models import pedidos, clientes_emails
from datetime import datetime, date, timedelta
from .forms import FormActualizarPedidos, FormMailReceptor, FormCuerpoMail, FormSelector, FormSelector1, FormSelector2, FormSelector3, FormSelector4, FormSelector5, FormSelector6, FormSelector7, FormSelector8, FormSelector9, FormSelector10, FormSelector11, FormSelector12, FormCrearCliente, FormCrearPedido, FormCambiarEstado, FormAsignarHR
from .funciones import mail_primera_instancia
from django.contrib.auth.decorators import login_required

formato_fecha = "%d/%m/%Y %H:%M:%S"
formato_fecha2 = "%d/%m/%Y"
hoy = datetime.today()
dia = hoy.day
mes = hoy.month
anio = hoy.year
fecha_hoy = str(dia) + '/' + str(mes) + '/' + str(anio)
fecha_hoy_f = datetime.strptime(fecha_hoy, formato_fecha2)
# Create your views here.





@login_required
def sincronizar(request):
    
    hace_3_dias = date.today() - timedelta(days=100)
    
    pedidos_saladillo = pedidos.objects.all()
    
    lista_pedidos_nuevos = pedidos_saladillo.filter(fecha__range=[hace_3_dias , date.today()])
    
    
    lista_pedidos_viejos = PedidoParaMail.objects.all()
    maestro_cliente = MaestroCliente.objects.all()
    contador = 0
    for valor in lista_pedidos_nuevos:
        filtro = lista_pedidos_viejos.filter(nro_pedido=valor.numero)
        if not filtro:
            cliente_nombre = maestro_cliente.filter(codigo=valor.codigo_cliente)
            
            if cliente_nombre:
                desc = MaestroCliente.objects.get(codigo=valor.codigo_cliente)
                cliente = desc.nombre
                num_celu = desc.num_celular
            else:
                cliente = 'Sin Datos'
                num_celu = 'Sin Datos'
            
            nuevo_pedido = PedidoParaMail(
                codigo_cliente = valor.codigo_cliente,
                cliente = cliente,
                nro_pedido = valor.numero,
                importe_total = valor.importe_total_comprobante,
                orden_de_compra = valor.ordendecompra,
                fecha_creacion = valor.fecha,
                fecha_estado = date.today(),
                estado = 'Recibido',
                estado_2 = '',
                estado_3 = '',
                estado_4 = '',
                num_celular = num_celu
                
            )
        
            nuevo_pedido.save()
            contador += 1
        
        
        
        
    
    
    
    
    
    
    msj = "Bases de datos actualizadas. Se han leido un total de "+str(len(lista_pedidos_nuevos))+" pedidos y se han actualizado un total de " + str(contador) + " pedidos nuevos desde la fecha " + str(hace_3_dias) + " hasta " + str(date.today())
    
    return render(request, 'saladillo/sincronizar.html', {
        'msj':msj
        })
        








def asignar_hr_masiva(request, id):
    
    pedido = PedidoParaMail.objects.get(id=id)
    
    nro_de_ruta = pedido.nro_ruteo
    
    actualizar = PedidoParaMail.objects.filter(nro_ruteo=nro_de_ruta)
    
    if actualizar:
        
        for valor in actualizar:
            pedido_actualizable = PedidoParaMail.objects.get(id=valor.id)
            print(pedido_actualizable)
    
    
    return render(request, 'Saladillo/asignar_hr_masiva.html')

@login_required
def asignar_hr(request, id):
    form_asignar_hr = FormAsignarHR()
    filtro = PedidoParaMail.objects.filter(id=id)
    
    
    
    
    if not filtro:
        msj = 'ID Inexistente'
        return render(request, 'saladillo/asignar_hr.html', {'msj':msj, 'form':form_asignar_hr})
    
    pedido = PedidoParaMail.objects.get(id=id)
    cliente = str(pedido.cliente)
    nro_pedido = str(pedido.nro_pedido)
    form_asignar_hr = FormAsignarHR()
    
    if request.method == 'POST':
        
        form_asignacion = FormAsignarHR(request.POST)
        
        if form_asignacion.is_valid():
            info = form_asignacion.cleaned_data
            filtro2 = HojaRuta.objects.filter(nro_pedido=pedido.nro_pedido)
            
            if filtro2:
                nro_pedido = pedido.nro_pedido
                actualizar = HojaRuta.objects.get(nro_pedido=nro_pedido)
                actualizar.nro_hoja_de_ruta = info['nro_hoja_de_ruta']
                actualizar.transportista = str(info['transportista'])
                actualizar.estado_en_hr = 'En Carga'
                pedido.nro_ruteo = info['nro_hoja_de_ruta']
                pedido.estado = 'Recibido'
                pedido.estado_2 = 'Preparado'
                pedido.estado_3 = 'Ruteado'
                pedido.estado_4 = ""
                
                
                
                
                pedido.save()
                actualizar.save()
                msj = 'El pedido nro ' + str(nro_pedido) + ' ya se encuentra asignado a una HR. Se ha modificado a la HR nro: ' + str(info['nro_hoja_de_ruta'])
                
                
                return render(request, 'saladillo/asignar_hr.html', {'msj':msj, 'form':form_asignar_hr, 'id':id})
            
        
            nueva_asgignacion = HojaRuta(
                nro_hoja_de_ruta = info['nro_hoja_de_ruta'],
                transportista = info['transportista'],
                nro_pedido = pedido.nro_pedido
            )
            pedido.nro_ruteo = info['nro_hoja_de_ruta']
            pedido.estado = "Recibido"
            pedido.estado_2 = "Preparado"
            pedido.estado_3 = "Ruteado"
            pedido.estado_4 = ""
            pedido.save()
            
            nueva_asgignacion.save()
            
            msj = 'El pedido ' + str(nro_pedido) + ' ha sido asignado a la HR nro: ' + str(info['nro_hoja_de_ruta'])
            
            
            return render(request, 'saladillo/asignar_hr.html', {'msj':msj, 'form':form_asignar_hr, 'id':id})
        else:
            
            msj = 'Formulario invalido'
            return render(request, 'saladillo/asignar_hr.html', {'msj':msj, 'form':form_asignar_hr, 'id':id})
    
    
    
    
    
    
    id = id
    msj = 'Asignacion a HR para pedido ' + nro_pedido + ' ' + cliente
    return render(request, 'saladillo/asignar_hr.html', {'msj':msj, 'form':form_asignar_hr, 'id':id})
    



@login_required
def panel_chofer(request):
    
    
    
    
    
    
    msj = "Bienvenido"
    user = request.user
    
    transportista = str(user)
    lista_de_hr = []
    iniciar_hr = []
        
    hojas = HojaRuta.objects.all()
    hojas_asignadas = hojas.filter(transportista=transportista)
    pedidos = PedidoParaMail.objects.all()
    clientes = MaestroCliente.objects.all()
    
    for valor in hojas_asignadas:
        
        pedido = pedidos.filter(nro_pedido=valor.nro_pedido)
        
        for valor1 in pedido:
            
            if valor1.estado_4 == "":
                
                lista_de_hr.append(valor1)
                
    for hr in hojas_asignadas:
        nro_hr = hr.nro_hoja_de_ruta
        
        if not nro_hr in iniciar_hr:
            iniciar_hr.append(nro_hr)
                

    
    if lista_de_hr:
        msj = "Resultado:"
        return render(request, 'saladillo/panel_chofer.html', {'msj':msj,
                                                               'lista_de_hr':lista_de_hr,
                                                               'iniciar_hr':iniciar_hr
                                                           })
        
    else:
        msj = "Sin resultado de busqueda."
        return render(request, 'saladillo/panel_chofer.html', {'msj':msj,
                                                               
                                                               
                                                               
                                                           })
    
    
    



@login_required
def subir_estado(request, id):
    form_asignar_hr = FormAsignarHR()
    pedido = PedidoParaMail.objects.get(id=id)
    if pedido.estado == 'Recibido' and pedido.estado_2 == '' and pedido.estado_3 == '' and pedido.estado_4 == '':
        pedido.estado_2 = 'Preparado'
        pedido.save()
        msj = 'Cambio de estado correcto. El pedido pasa a Preparado'
        lista_1 = PedidoParaMail.objects.filter(estado_4="")
        lista_2 = lista_1.filter(estado_3="")
        lista_3 = lista_2.filter(estado_2='')
        
        
        lista_pedidos_recibidos = lista_3.filter(estado='Recibido')
        lista_pedidos_preparados = lista_2.filter(estado_2='Preparado')
        lista_pedidos_ruteado = lista_1.filter(estado_3='Ruteado')
        lista_pedidos_entregado = PedidoParaMail.objects.filter(estado_4='Entregado')
        form_crear_pedido = FormCrearPedido()
        return render(request, 'saladillo/sector_pruebas.html', {'form_crear_pedido':form_crear_pedido,
                                                             'lista_pedidos_recibidos':lista_pedidos_recibidos,
                                                             'lista_pedidos_preparados':lista_pedidos_preparados,
                                                             'lista_pedidos_ruteado': lista_pedidos_ruteado,
                                                             'lista_pedidos_entregado': lista_pedidos_entregado,
                                                             'msj':msj,
                                                             'form_asignar_hr':form_asignar_hr
                                                             })
    
    elif pedido.estado == 'Recibido' and pedido.estado_2 == 'Preparado' and pedido.estado_3 == '' and pedido.estado_4 == '':
        
        
        pedido.estado_3 = 'Ruteado'
        
        
        
        pedido.save()
        msj = 'Cambio de estado correcto. El pedido pasa a Ruteado'
        lista_1 = PedidoParaMail.objects.filter(estado_4="")
        lista_2 = lista_1.filter(estado_3="")
        lista_3 = lista_2.filter(estado_2='')
        
        
        lista_pedidos_recibidos = lista_3.filter(estado='Recibido')
        lista_pedidos_preparados = lista_2.filter(estado_2='Preparado')
        lista_pedidos_ruteado = lista_1.filter(estado_3='Ruteado')
        lista_pedidos_entregado = PedidoParaMail.objects.filter(estado_4='Entregado')
        form_crear_pedido = FormCrearPedido()
        return render(request, 'saladillo/sector_pruebas.html', {'form_crear_pedido':form_crear_pedido,
                                                             'lista_pedidos_recibidos':lista_pedidos_recibidos,
                                                             'lista_pedidos_preparados':lista_pedidos_preparados,
                                                             'lista_pedidos_ruteado': lista_pedidos_ruteado,
                                                             'lista_pedidos_entregado': lista_pedidos_entregado,
                                                             'msj':msj,
                                                             'form_asignar_hr':form_asignar_hr
                                                             })
        
        
    elif pedido.estado == 'Recibido' and pedido.estado_2 == 'Preparado' and pedido.estado_3 == 'Ruteado' and pedido.estado_4 == '':
        pedido.estado_4 = 'Entregado'
        pedido.save()
        msj = 'Cambio de estado correcto. El pedido pasa a Entregado'
        lista_1 = PedidoParaMail.objects.filter(estado_4="")
        lista_2 = lista_1.filter(estado_3="")
        lista_3 = lista_2.filter(estado_2='')
        
        
        lista_pedidos_recibidos = lista_3.filter(estado='Recibido')
        lista_pedidos_preparados = lista_2.filter(estado_2='Preparado')
        lista_pedidos_ruteado = lista_1.filter(estado_3='Ruteado')
        lista_pedidos_entregado = PedidoParaMail.objects.filter(estado_4='Entregado')
        form_crear_pedido = FormCrearPedido()
        return render(request, 'saladillo/sector_pruebas.html', {'form_crear_pedido':form_crear_pedido,
                                                             'lista_pedidos_recibidos':lista_pedidos_recibidos,
                                                             'lista_pedidos_preparados':lista_pedidos_preparados,
                                                             'lista_pedidos_ruteado': lista_pedidos_ruteado,
                                                             'lista_pedidos_entregado': lista_pedidos_entregado,
                                                             'msj':msj,
                                                             'form_asignar_hr':form_asignar_hr
                                                             })
    else:
        msj = 'Error en el cambio de estado, el pedido tiene estados salteados'
        lista_1 = PedidoParaMail.objects.filter(estado_4="")
        lista_2 = lista_1.filter(estado_3="")
        lista_3 = lista_2.filter(estado_2='')
        
        
        lista_pedidos_recibidos = lista_3.filter(estado='Recibido')
        lista_pedidos_preparados = lista_2.filter(estado_2='Preparado')
        lista_pedidos_ruteado = lista_1.filter(estado_3='Ruteado')
        lista_pedidos_entregado = PedidoParaMail.objects.filter(estado_4='Entregado')
        form_crear_pedido = FormCrearPedido()
        return render(request, 'saladillo/sector_pruebas.html', {'form_crear_pedido':form_crear_pedido,
                                                             'lista_pedidos_recibidos':lista_pedidos_recibidos,
                                                             'lista_pedidos_preparados':lista_pedidos_preparados,
                                                             'lista_pedidos_ruteado': lista_pedidos_ruteado,
                                                             'lista_pedidos_entregado': lista_pedidos_entregado,
                                                             'msj':msj,
                                                             'form_asignar_hr':form_asignar_hr
                                                             })
    

@login_required
def bajar_estado(request, id):
    form_asignar_hr = FormAsignarHR()
    pedido = PedidoParaMail.objects.get(id=id)
    
    if pedido.estado == 'Recibido' and pedido.estado_2 == 'Preparado' and pedido.estado_3 == 'Ruteado' and pedido.estado_4 == 'Entregado':
        pedido.estado_4 = ''
        pedido.save()
        msj = 'Cambio de estado correcto, el pedido pasa a estar Ruteado'
        lista_1 = PedidoParaMail.objects.filter(estado_4="")
        lista_2 = lista_1.filter(estado_3="")
        lista_3 = lista_2.filter(estado_2='')
        
        
        lista_pedidos_recibidos = lista_3.filter(estado='Recibido')
        lista_pedidos_preparados = lista_2.filter(estado_2='Preparado')
        lista_pedidos_ruteado = lista_1.filter(estado_3='Ruteado')
        lista_pedidos_entregado = PedidoParaMail.objects.filter(estado_4='Entregado')
        form_crear_pedido = FormCrearPedido()
        return render(request, 'saladillo/sector_pruebas.html', {'form_crear_pedido':form_crear_pedido,
                                                             'lista_pedidos_recibidos':lista_pedidos_recibidos,
                                                             'lista_pedidos_preparados':lista_pedidos_preparados,
                                                             'lista_pedidos_ruteado': lista_pedidos_ruteado,
                                                             'lista_pedidos_entregado': lista_pedidos_entregado,
                                                             'msj':msj,
                                                             'form_asignar_hr':form_asignar_hr
                                                             })
        
    elif pedido.estado == 'Recibido' and pedido.estado_2 == 'Preparado' and pedido.estado_3 == 'Ruteado' and pedido.estado_4 == '':
        pedido.estado_3 = ''
        pedido.save()
        msj = 'Cambio de estado correcto, el pedido pasa a estar Preparado'
        lista_1 = PedidoParaMail.objects.filter(estado_4="")
        lista_2 = lista_1.filter(estado_3="")
        lista_3 = lista_2.filter(estado_2='')
        
        
        lista_pedidos_recibidos = lista_3.filter(estado='Recibido')
        lista_pedidos_preparados = lista_2.filter(estado_2='Preparado')
        lista_pedidos_ruteado = lista_1.filter(estado_3='Ruteado')
        lista_pedidos_entregado = PedidoParaMail.objects.filter(estado_4='Entregado')
        form_crear_pedido = FormCrearPedido()
        return render(request, 'saladillo/sector_pruebas.html', {'form_crear_pedido':form_crear_pedido,
                                                             'lista_pedidos_recibidos':lista_pedidos_recibidos,
                                                             'lista_pedidos_preparados':lista_pedidos_preparados,
                                                             'lista_pedidos_ruteado': lista_pedidos_ruteado,
                                                             'lista_pedidos_entregado': lista_pedidos_entregado,
                                                             'msj':msj,
                                                             'form_asignar_hr':form_asignar_hr
                                                             })
    elif pedido.estado == 'Recibido' and pedido.estado_2 == 'Preparado' and pedido.estado_3 == '' and pedido.estado_4 == '':
        pedido.estado_2 = ''
        pedido.save()
        msj = 'Cambio de estado correcto, el pedido pasa a estar Recibido'
        lista_1 = PedidoParaMail.objects.filter(estado_4="")
        lista_2 = lista_1.filter(estado_3="")
        lista_3 = lista_2.filter(estado_2='')
        
        
        lista_pedidos_recibidos = lista_3.filter(estado='Recibido')
        lista_pedidos_preparados = lista_2.filter(estado_2='Preparado')
        lista_pedidos_ruteado = lista_1.filter(estado_3='Ruteado')
        lista_pedidos_entregado = PedidoParaMail.objects.filter(estado_4='Entregado')
        form_crear_pedido = FormCrearPedido()
        return render(request, 'saladillo/sector_pruebas.html', {'form_crear_pedido':form_crear_pedido,
                                                             'lista_pedidos_recibidos':lista_pedidos_recibidos,
                                                             'lista_pedidos_preparados':lista_pedidos_preparados,
                                                             'lista_pedidos_ruteado': lista_pedidos_ruteado,
                                                             'lista_pedidos_entregado': lista_pedidos_entregado,
                                                             'msj':msj,
                                                             'form_asignar_hr':form_asignar_hr
                                                             })
    
    else:
        msj = 'Error en el pedido, tiene estados salteados'
        lista_1 = PedidoParaMail.objects.filter(estado_4="")
        lista_2 = lista_1.filter(estado_3="")
        lista_3 = lista_2.filter(estado_2='')
        
        
        lista_pedidos_recibidos = lista_3.filter(estado='Recibido')
        lista_pedidos_preparados = lista_2.filter(estado_2='Preparado')
        lista_pedidos_ruteado = lista_1.filter(estado_3='Ruteado')
        lista_pedidos_entregado = PedidoParaMail.objects.filter(estado_4='Entregado')
        form_crear_pedido = FormCrearPedido()
        return render(request, 'saladillo/sector_pruebas.html', {'form_crear_pedido':form_crear_pedido,
                                                             'lista_pedidos_recibidos':lista_pedidos_recibidos,
                                                             'lista_pedidos_preparados':lista_pedidos_preparados,
                                                             'lista_pedidos_ruteado': lista_pedidos_ruteado,
                                                             'lista_pedidos_entregado': lista_pedidos_entregado,
                                                             'msj':msj,
                                                             'form_asignar_hr':form_asignar_hr
                                                             })
    
    
    
    
@login_required
def sector_pruebas(request):
    msj = 'Bienvenido'
    form_asignar_hr = FormAsignarHR()
    if request.method == 'POST':
        
        if'btn_crear_pedido' in request.POST:
            form_crear_pedido = FormCrearPedido(request.POST)
            if form_crear_pedido.is_valid():
                info = form_crear_pedido.cleaned_data
                nuevo_pedido = PedidoParaMail(
                    codigo_cliente = info['codigo_cliente'],
                    cliente = info['cliente'],
                    nro_pedido = info['nro_pedido'],
                    cantidad = 12,
                    mail = info['mail'],
                    mail1_enviado = 0,
                    mail2_enviado = 0,
                    mail3_enviado = 0,
                    entregado = 0,
                    importe_total = 1,
                    orden_de_compra = info['oc'],
                    estado = 'Recibido',
                    estado_2 = '',
                    estado_3 = '',
                    estado_4 = '',
                    localidad = info['localidad'],
                    
                    domicilio = info['domicilio'],
                    cp = info['cp'],
                    
                    fecha_creacion = date.today(),
                    fecha_estado = date.today()
                )
                nuevo_pedido.save()
                msj = 'Pedido creado correctamente'
            else:
                msj = 'Formulario invalido'
                return render(request, 'saladillo/sector_pruebas.html', {'form_crear_pedido':form_crear_pedido,
                                                             'lista_pedidos_recibidos':lista_pedidos_recibidos,
                                                             'lista_pedidos_preparados':lista_pedidos_preparados,
                                                             'lista_pedidos_ruteado': lista_pedidos_ruteado,
                                                             'lista_pedidos_entregado': lista_pedidos_entregado,
                                                             'msj':msj,
                                                             'form_asignar_hr':form_asignar_hr
                                                             })
    
    lista_1 = PedidoParaMail.objects.filter(estado_4="")
    print(len(lista_1))
    lista_2 = lista_1.filter(estado_3="")
    lista_3 = lista_2.filter(estado_2='')
    
    
    lista_pedidos_recibidos = lista_3.filter(estado='Recibido')
    lista_pedidos_preparados = lista_2.filter(estado_2='Preparado')
    lista_pedidos_ruteado = lista_1.filter(estado_3='Ruteado')
    lista_pedidos_entregado = PedidoParaMail.objects.filter(estado_4='Entregado')
    form_crear_pedido = FormCrearPedido()
    
    
    
    
    return render(request, 'saladillo/sector_pruebas.html', {'form_crear_pedido':form_crear_pedido,
                                                             'lista_pedidos_recibidos':lista_pedidos_recibidos,
                                                             'lista_pedidos_preparados':lista_pedidos_preparados,
                                                             'lista_pedidos_ruteado': lista_pedidos_ruteado,
                                                             'lista_pedidos_entregado': lista_pedidos_entregado,
                                                             'msj':msj,
                                                             'form_asignar_hr':form_asignar_hr
                                                             })

@login_required
def mail_receptor(request):
    
    
    if request.method == "POST":
        form = FormMailReceptor(request.POST)
        if form.is_valid():
            
            info = form.cleaned_data
            
            mail_viejo = MailReceptor.objects.filter(id=1)
            if mail_viejo:
                nuevo_receptor = info["mail"]
                mail_viej0 = MailReceptor.objects.get(id=1)
                mail_viej0.mail = nuevo_receptor
                mail_viej0.save()
                msj = "Mail Editado correctamente"
                
            
                
                return render(request, "saladillo/mail_receptor.html", {'msj':msj, 'form':form})
            
            else:
                nuevo_receptor = MailReceptor(mail=info["mail"])
                nuevo_receptor.save()
                msj = "Mail creado exitosamente"
            
                return render(request, "saladillo/mail_receptor.html", {"msj":msj,'form':form})
    else:
        
        mail_en_base = MailReceptor.objects.filter(id=1)
        
        if not mail_en_base:
            form = FormMailReceptor(initial={'mail':"info@saladillo.com.ar"})
        else:
            mail = MailReceptor.objects.get(id=1)
            
            form = FormMailReceptor(initial={'mail':str(mail.mail)})
        return render(request, "saladillo/mail_receptor.html", {"form":form})


@login_required
def config_mail_1(request):
    
    form = FormCuerpoMail()
    form_selector = FormSelector()
    form_selector1 = FormSelector1()
    form_selector2 = FormSelector2()
    form_selector3 = FormSelector3()
    form_selector4 = FormSelector4()
    form_selector5 = FormSelector5()
    form_selector6 = FormSelector6()
    form_selector7 = FormSelector7()
    form_selector8 = FormSelector8()
    form_selector9 = FormSelector9()
    form_selector10 = FormSelector10()
    form_selector11 = FormSelector11()
    form_selector12 = FormSelector12()
    
    if request.method == 'POST':
        form = FormCuerpoMail(request.POST)
        
        info = request.POST
        #print(info)
        print(info['selector'])
        
        if form.is_valid():
            informacion = form.cleaned_data
            
            #print(informacion)
            
            concatenado = informacion['body_uno']
            
            #print(concatenado)
            
            
            return render(request, 'saladillo/config_mail.html', {'form':form, 
                                                                  'form_selector':form_selector, 
                                                                  'form_selector1':form_selector1, 
                                                                  'form_selector2':form_selector2, 
                                                                  'form_selector3':form_selector3, 
                                                                  'form_selector4':form_selector4, 
                                                                  'form_selector5':form_selector5, 
                                                                  'form_selector6':form_selector6, 
                                                                  'form_selector7':form_selector7, 
                                                                  'form_selector8':form_selector8, 
                                                                  'form_selector9':form_selector9, 
                                                                  'form_selector10':form_selector10, 
                                                                  'form_selector11':form_selector11, 
                                                                  'form_selector12':form_selector12
                                                                  })
            
            
            
        else:
            
            msj_error = 'Formulario inválido'
            print('error')
            return render(request, 'saladillo/config_mail.html', {'form':form, 
                                                                  'form_selector':form_selector, 
                                                                  'form_selector1':form_selector1, 
                                                                  'form_selector2':form_selector2, 
                                                                  'form_selector3':form_selector3, 
                                                                  'form_selector4':form_selector4, 
                                                                  'form_selector5':form_selector5, 
                                                                  'form_selector6':form_selector6, 
                                                                  'form_selector7':form_selector7, 
                                                                  'form_selector8':form_selector8, 
                                                                  'form_selector9':form_selector9, 
                                                                  'form_selector10':form_selector10, 
                                                                  'form_selector11':form_selector11, 
                                                                  'form_selector12':form_selector12
                                                                  })
        
        
    
    else:
        
        
        
        form = FormCuerpoMail()
        form_selector = FormSelector()
        form_selector1 = FormSelector1()
        form_selector2 = FormSelector2()
        form_selector3 = FormSelector3()
        form_selector4 = FormSelector4()
        form_selector5 = FormSelector5()
        form_selector6 = FormSelector6()
        form_selector7 = FormSelector7()
        form_selector8 = FormSelector8()
        form_selector9 = FormSelector9()
        form_selector10 = FormSelector10()
        form_selector11 = FormSelector11()
        form_selector12 = FormSelector12()
        
        return render(request, 'saladillo/config_mail.html', {'form':form, 
                                                              'form_selector':form_selector, 
                                                              'form_selector1':form_selector1, 
                                                              'form_selector2':form_selector2, 
                                                              'form_selector3':form_selector3, 
                                                              'form_selector4':form_selector4, 
                                                              'form_selector5':form_selector5, 
                                                              'form_selector6':form_selector6, 
                                                              'form_selector7':form_selector7, 
                                                              'form_selector8':form_selector8, 
                                                              'form_selector9':form_selector9, 
                                                              'form_selector10':form_selector10, 
                                                              'form_selector11':form_selector11, 
                                                              'form_selector12':form_selector12
                                                              })
    
    
    



@login_required
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
                return render(request, 'saladillo/index_saladillo.html', {'msj_carga':msj_carga, 
                                                                          'pedidos':pedidos_cargados, 
                                                                          'form':form, 
                                                                          'form2':form2
                                                                          })
            

            
            elif 'btn_enviar_mail' in request.POST:
                
                un_dia = form.cleaned_data
                pendientes_totales = PedidoParaMail.objects.filter(fecha_creacion=un_dia['fecha'])
                total_sin_datos = 0
                total_enviados = 0
                
                if pendientes_totales:
                    for valor in pendientes_totales:
                        if valor.mail == 'Sin Datos':
                            total_sin_datos += 1
                            
                        else:
                            
                            cli = valor.cliente
                            print(cli)
                            mail_primera_instancia(cli, 
                                                   importe_total=valor.importe_total, 
                                                   mail=valor.mail, 
                                                   orden_de_compra=valor.orden_de_compra, 
                                                   nro_pedido=valor.nro_pedido, 
                                                   ins1=valor.mail1_enviado, 
                                                   ins2=valor.mail2_enviado, 
                                                   ins3=valor.mail3_enviado,
                                                   estado=valor.entregado)
                            total_enviados += 1
                            valor.mail1_enviado = 'Si'
                            
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





@login_required
def monitor(request):
    
    enviados = PrimeraInstancia.objects.all()
    
    pendientes = PedidoParaMail.objects.filter(mail1_enviado=False)
    
    
    return render(request, 'saladillo/monitor.html',{'enviados':len(enviados), 'pendientes':len(pendientes)})