from django.shortcuts import render

from .models import PedidoParaMail, MaestroCliente, PrimeraInstancia, MailReceptor, CuerpoMail
from stg.models import pedidos, clientes_emails
from datetime import datetime, date
from .forms import FormActualizarPedidos, FormMailReceptor, FormCuerpoMail, FormSelector, FormSelector1, FormSelector2, FormSelector3, FormSelector4, FormSelector5, FormSelector6, FormSelector7, FormSelector8, FormSelector9, FormSelector10, FormSelector11, FormSelector12
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



def config_mail_1(request):
    
    if request.method == 'POST':
        form = FormCuerpoMail(request.POST)
        
        if form.is_valid():
            informacion = form.cleaned_data
            
        else:
            
            msj_error = 'Formulario inválido'
            return render(request, 'saladillo/config_mail.html', {'msj_error':msj_error})    
        
        return render(request, 'saladillo/config_mail.html', {'msj_carga':'POST'})
    
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
        
        return render(request, 'saladillo/config_mail.html', {'form':form, 'form_selector':form_selector, 'form_selector1':form_selector1, 'form_selector2':form_selector2, 'form_selector3':form_selector3, 'form_selector4':form_selector4, 'form_selector5':form_selector5, 'form_selector6':form_selector6, 'form_selector7':form_selector7, 'form_selector8':form_selector8, 'form_selector9':form_selector9, 'form_selector10':form_selector10, 'form_selector11':form_selector11, 'form_selector12':form_selector12})
    
    
    




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






def monitor(request):
    
    enviados = PrimeraInstancia.objects.all()
    
    pendientes = PedidoParaMail.objects.filter(mail1_enviado=False)
    
    
    return render(request, 'saladillo/monitor.html',{'enviados':len(enviados), 'pendientes':len(pendientes)})