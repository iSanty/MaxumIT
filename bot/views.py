from django.shortcuts import render
from .models import Punto

from lecturas_db.models import stg_pedidos
from stg.models import pedidos as TablaSaladillo
from accounts.models import MasDatosUsuario

# Create your views here.
from saladillo.models import PedidoParaMail
from django.shortcuts import render
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import os
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
load_dotenv()

import smtplib

import random


def validar_dato(consulta):
    
    for digito in consulta:
        if digito in '0123456789':
            continue
        else:
            return False
    return True





account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')

client = Client(account_sid, auth_token)


def bot_saladillo(request):
    
    
    if request.method =="POST":
        
        #Esta info trae el mensaje
        mensaje = request.POST["Body"]
        numero = request.POST["From"]
        numero_limpio = numero[13:23]
        pedidos_cliente = []
        #Agarro la informacion del nro de telefono, pedudos, datos de usuario y estado de consulta "punto"
        punto = Punto.objects.filter(numero=numero)
        datos_usuario = MasDatosUsuario.objects.filter(num_celular=numero_limpio)
        if len(datos_usuario) == 1:
            datos_usuario_get = MasDatosUsuario.objects.get(num_celular=numero_limpio)
            pedidos_cliente = PedidoParaMail.objects.filter(codigo_cliente=datos_usuario_get.codigo_cliente)
            
        elif len(datos_usuario) >= 1 or len(datos_usuario) <= 1:
            datos_usuario_get = ''
        
        
        #Este seria el login, si no tiene asignado un nro de celular, disparo el mensaje para los NO REGISTRADOS
        if datos_usuario_get != '':
            
            
            
            
            
            
            
            #Si el usuario manda el mensaje con la palabra inicio, se reinicia la tabla "Punto"
            if mensaje == 'Inicio' or mensaje == 'inicio' or mensaje == 'INICIO' or mensaje == 'INicio' or mensaje == 'iNICIO' or mensaje == 'INICIo':
                if punto:
                    punto = Punto.objects.get(numero=numero)
                    punto.punto = 'Principio'
                    punto.cons_pedido = 1 #Aca guardo el nro de pedido para dsps consultar por articulo
                    punto.save()
                else:
                    nuevo_numero = Punto(
                        punto = 'Principio',
                        cons_pedido = 1,
                        numero = numero
                    )
                    nuevo_numero.save()
                client.messages.create(
                    from_='whatsapp:+14155238886',
                    body="""Paramentros reiniciados.
Bienvenido, por favor responda con el número de la opción deseada:
1) Contultar estado por numero de pedido
2) Consultas por articulo
                    """,
                    to=numero
                )
                return HttpResponse('')
                #hasta aca el proceso de la palabra INICIO
                    
            #Aca lo corto si no tiene cliente asignado, le pregunto por el CUIL para iniciar el bot sin registro
            if pedidos_cliente == []:
                if len(pedidos_cliente) == 1:
                    codigo_cliente_cuerpo = str(pedidos_cliente.codigo_cliente)
                else:
                    codigo_cliente_cuerpo = '"Sin registro"'
                client.messages.create(
                    from_='whatsapp:+14155238886',
                    body="Estimado cliente, no se han encontrado pedidos cargados, Su codigo de cliente es: " + codigo_cliente_cuerpo + " - Verifique y vuelva a intentarlo",
                    to=numero
                )
                return HttpResponse('')
                
                
            ##### Bloque Principal
            punto = Punto.objects.get(numero=numero)
            
            
            #Si el punto, es como el "punto de consulta", si es igual a 1 quiere decir que recien empieza, sino dsps pasa por otras palabras
            if punto.punto == "1":
                punto.punto = 'Principio'
                
                client.messages.create(
                    from_='whatsapp:+14155238886',
                    body="Bienvenido, usted tiene un total de " + str(len(pedidos_cliente)) + " pedidos cargados. Que desea consultar?",
                    to=numero
                )
                client.messages.create(
                        from_='whatsapp:+14155238886',
                        body="Para volver a empezar, envie la palabra inicio en cualquier momento.",
                        to=numero
                    )
                client.messages.create(
                    from_='whatsapp:+14155238886',
                    body="""1) Contultar estado por numero de pedido
2) Consultas por articulo
                    """,
                    to=numero
                )
                punto.save()
                
                return HttpResponse('')
                
            elif punto.punto == "Principio":
                if mensaje == '1':
                    punto.punto = 'ConsultaPedido'
                    punto.save()
                    client.messages.create(
                        from_='whatsapp:+14155238886',
                        body="Por favor indique su nro de pedido.",
                        to=numero
                    )
                    return HttpResponse('')
                elif mensaje == '2':
                    punto.punto = 'ConsultaArticulo'
                    punto.save()
                    client.messages.create(
                        from_='whatsapp:+14155238886',
                        body="Indique el nro de pedido para consultar si contiene un articulo.",
                        to=numero
                    )
                    return HttpResponse('')
                else:
                    punto.punto = 'Principio'
                    punto.save()
                    client.messages.create(
                        from_='whatsapp:+14155238886',
                        body="""Opcion incorrecta.
1) Contultar estado por numero de pedido
2) Consultas por articulo
                        """,
                        to=numero
                    )
                    return HttpResponse('')
            elif punto.punto == 'ConsultaPedido':
                validar_pedido = validar_dato(mensaje)#Me fijo si es numerico
                
                if validar_pedido:
                    pedido_consultado = int(mensaje)
                    
                    pedido_ok = "No"
                    for valor in pedidos_cliente:
                        if valor.nro_pedido == pedido_consultado:
                            pedido_ok = "OK"
                        
                    
                    
                    if pedido_ok == "No":
                        client.messages.create(
                            from_='whatsapp:+14155238886',
                            body="El nro de pedido " + str(pedido_consultado) + ' no se encuentra bajo su codigo de cliente '+ str(datos_usuario_get.codigo_cliente) + ' o es inexistente. Reingrese un numero valido o para volver envie "inicio"',
                            to=numero
                        )
                        return HttpResponse('')
               
                    pedido = PedidoParaMail.objects.get(nro_pedido=pedido_consultado)
                    
                    if pedido.estado_4 == 'Entregado':
                        cuerpo = 'Su pedido ha sido entregado el dia ' + str(pedido.fecha_estado_4) + ". Muchas gracias por elegirnos, para consultar otro pedido escriba el nunmero o la palabra inicio para volver."
                    elif pedido.estado_3 == 'Ruteado':
                        cuerpo = 'Su pedido se encuentra en viaje! Es el nro #gmapi.orden# en la lista y el transporte se encuentra por la zona de #gmapi.localidad#. En aproximadamente #gmapi.tiempo_entrega_aproximado# estaremos visitandote en tu domicilio registrado. Para consultar otro escriba el numero o la palabra inicio para volver.'
                    elif pedido.estado_2 == 'Preparado':
                        cuerpo = 'Su pedido nro ' + str(pedido.nro_pedido) + ' ya ha sido preparado, en menos de 24hs habiles se le asignara un transporte. Para consultar otro pedido escriba el numero o la palabra inicio para volver al menu principal.'
                    elif pedido.estado == 'Recibido':
                        cuerpo = 'Su pedido ' + str(pedido.nro_pedido) + ' ha ingresado en nuestra base de datos el ' + str(pedido.fecha_estado) + ' y se encuentra en estado "Recibido". En menos de 24hs habiles pasará a estar entregado. Envie "inicio" para volver o un numero de pedido para consultar.'
                        
                        
                    client.messages.create(
                        from_='whatsapp:+14155238886',
                        body=cuerpo,
                        to=numero
                    )
                    return HttpResponse('')
                else:
                    
                    client.messages.create(
                        from_='whatsapp:+14155238886',
                        body="El nro de pedido debe ser numerico, reintente! o escriba inicio para volver.",
                        to=numero
                    )
                
                    return HttpResponse('bot de wp')
                
                    
                
            elif punto.punto == "ConsultaArticulo" and punto.cons_pedido == 1:
                
                pedido_numerico = validar_dato(mensaje)
                
                if pedido_numerico:
                    punto = Punto.objects.get(numero=numero)
                    punto.cons_pedido = int(mensaje)
                    
                    validar_pedido = TablaSaladillo.objects.filter(numero=int(mensaje))
                    punto.save()
                    
                    if validar_pedido:
                        
                        client.messages.create(
                            from_='whatsapp:+14155238886',
                            body="Ingrese el artículo: ",
                            to=numero
                        )
                    else:
                        punto.cons_pedido = 1
                        punto.save()
                        client.messages.create(
                            from_='whatsapp:+14155238886',
                            body="Pedido inexistente, reintente: ",
                            to=numero
                        )
                
                    return HttpResponse('bot de wp')
                    
            elif punto.punto == "ConsultaArticulo" and punto.cons_pedido != 1:
                
                pedido = Punto.objects.get(numero=numero)
                detalle_pedido = TablaSaladillo.objects.filter(numero=pedido.cons_pedido)
                lista_articulos = []
                
                for valor in detalle_pedido:
                    if valor.codigo_articulo == mensaje:
                        lista_articulos.append(valor.cantidad)
                        
            
                total = str(sum(lista_articulos))
                largo = str(len(lista_articulos))
                
                client.messages.create(
                        from_='whatsapp:+14155238886',
                        body="El articulo " + mensaje + " tiene un total de " + total + " unidades. El pedido contiene " + largo + " lineas de este articulo. Para consultar otro articulo del mismo pedido, escribalo, sino escriba inicio para volver.",
                        to=numero
                    )
                return HttpResponse('bot de wp')
                
                
            
            
            ##### Bloque Principal
            
            
            
                
                
                
                
                
                
                
                
                
                
                
                
        else:#este es el else de cuando no tengo un usuario con nro de celular
        
            client.messages.create(
                from_='whatsapp:+14155238886',
                body="Su nro de celular no se encuentra registrado, escriba su CUIL para iniciar el modo desconectado. Automaticamente se enviará una solicitud de registro al Administrador. Mientras tanto puede consultar el estado de sus pedidos.",
                to=numero
            )
            return HttpResponse('')
                
            
                    
                    
                    
                    
                    
                    
    return HttpResponse('')
            
            
    #         else:
    #             client.messages.create(
    #             from_='whatsapp:+14155238886',
    #             body="Bienvenido, usted tiene un total de  pedidos cargados. Que desea consultar?",
    #             to=numero
    #         )
    #         client.messages.create(
    #             from_='whatsapp:+14155238886',
    #             body="""1) Contultar estado por numero de pedido
    # 2) Consultas por articulo
    #             """,
    #             to=numero
    #         )
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
            
            
        #     if punto_existente.punto == 'inicio':
        #         if mensaje == '1':
        #             punto_existente.punto = 'ConsultaPedido'
        #             client.messages.create(
        #                 from_='whatsapp:+14155238886',
        #                 body="Indique el numero de pedido a consultar.",
        #                 to=numero
        #             )
        #             punto_existente.save()
        #             return HttpResponse
                
        #         elif mensaje == '2':
        #             print('es igual a 2')
        #         else:
        #             print('no soy 1 ni soy 2')
                    
        #     elif punto_existente.punto == 'ConsultaPedido':
                
        #         soy_un_pedido = validar_dato(mensaje)
                
        #         if soy_un_pedido:
        #             cliente = MasDatosUsuario.objects.filter(num_celular=numero_limpio)
        #             if cliente:
        #                 cliente = MasDatosUsuario.objects.get(num_celular=numero_limpio)
        #                 cliente_asignado = cliente.codigo_cliente
        #             else:
        #                 cliente_asignado = ''
                    
        #             nropedido = int(mensaje)
        #             pedido_consultado = PedidoParaMail.objects.filter(nro_pedido=nropedido)
        #             if pedido_consultado:
        #                 pedido_consultado = PedidoParaMail.objects.get(nro_pedido=nropedido)
        #                 ped = pedido_consultado.num_celular
        #             else:
        #                 ped = ''
                        
        #             if ped != cliente_asignado:
        #                 client.messages.create(
        #                 from_='whatsapp:+14155238886',
        #                 body="El pedido nro " + str(pedido_consultado) + ' se encuentra asignado a otro cliente, reintente',
        #                 to=numero
        #             )
                        
                        
                        
        #             if pedido_consultado:
        #                 ped_cons = PedidoParaMail.objects.get(nro_pedido=nropedido)
                        
        #                 # if ped_cons.num_celular != numero[13:23]:
        #                 #     client.messages.create(
        #                 #         from_='whatsapp:+14155238886',
        #                 #         body="El pedido no esta asociado a tu nro de celular. Reintente.",
        #                 #         to=numero
        #                 #     )
                    
        #                 #     return HttpResponse
                            
                        
                        
                        
                            
                            
        #                 
                
                    
        #         else:
        #             client.messages.create(
        #                 from_='whatsapp:+14155238886',
        #                 body="El nro de pedido debe ser numerico, reintente!",
        #                 to=numero
        #             )
        #             return HttpResponse('bot de wp')
                
                
                
                    
        
        # #### Primer Mensaje ##### #### Primer Mensaje ######### Primer Mensaje ######### Primer Mensaje ######### Primer Mensaje #####
        # else:
        #     nuevo = Punto(
        #         numero = numero,
        #         punto = 'inicio',
        #         cons_pedido = 1
        #         )
        #     nuevo.save()
        # punto = Punto.objects.get(numero=numero)
        # num_celular = numero[13:23]
        # lista_pedidos = PedidoParaMail.objects.filter(num_celular=num_celular)
#         client.messages.create(
#             from_='whatsapp:+14155238886',
#             body="Bienvenido, usted tiene un total de " + str(len(lista_pedidos)) + " pedidos cargados. Que desea consultar?",
#             to=numero
#         )
#         client.messages.create(
#             from_='whatsapp:+14155238886',
#             body="""1) Contultar estado por numero de pedido
# 2) Consultas por articulo
#             """,
#             to=numero
#         )
        #### Primer Mensaje ######### Primer Mensaje ######### Primer Mensaje ######### Primer Mensaje ######### Primer Mensaje #####
            
    
            
    
            
        
    



def bot(request):
    
    if request.method =="POST":
        
        mensaje = request.POST["Body"]
        numero = request.POST["From"]
        print(numero)
        #]punto = Punto.objects.filter(numero = numero)
        
        #if punto:
           # punto = Punto.objects.get(numero = numero)
        
            
                
            #if punto.punto == 'consulta_nro_pedido':
        lista_numerica = False
        if len(mensaje) > 2:
            lista_numerica = validar_dato(mensaje)
            
        
            
   
        
        if lista_numerica:
            mensaje = int(mensaje) 
            pedidos = PedidoParaMail.objects.filter(nro_pedido=mensaje)
        
        else:
            pedidos = False
            
        if pedidos:
            
            lista = []
            for valor in pedidos:
                
                if valor in lista:
                    return HttpResponse()
                else:
                    lista.append(valor)
                    if valor.estado == 'Recibido' and valor.estado_2 == 'Preparado' and valor.estado_3 == 'Ruteado' and valor.estado_4 == 'Entregado':
                        estado = 'Entregado'
                    elif valor.estado == 'Recibido' and valor.estado_2 == 'Preparado' and valor.estado_3 == 'Ruteado' and valor.estado_4 == '':
                        estado = 'Ruteado'
                    elif valor.estado == 'Recibido' and valor.estado_2 == 'Preparado' and valor.estado_3 == '' and valor.estado_4 == '':
                        estado = 'Preparado'
                    elif valor.estado == 'Recibido' and valor.estado_2 == '' and valor.estado_3 == '' and valor.estado_4 == '':
                        estado = 'Recibido'
                        
                        
                        
                    client.messages.create(
            from_='whatsapp:+14155238886',
            body="Su pedido nro " + str(valor.nro_pedido) + " se encuentra con estado " + estado,
            to=numero
        )
            return HttpResponse()
        
        
                    
        elif mensaje == '1':
            
            client.messages.create(
            from_='whatsapp:+14155238886',
            body="""Por favor escriba su numero de pedido.
""",
            to=numero
        )
            return HttpResponse()
            
            
            
            
        elif mensaje == '2':
            client.messages.create(
            from_='whatsapp:+14155238886',
            body="""Por favor indique su numero de cliente.
""",
            to=numero
        )
            return HttpResponse()
            
            
        
        
        client.messages.create(
            from_='whatsapp:+14155238886',
            body="""Hola, bienvenido al bot de Saladillo, responda con el numero de opcion deseada:
1: Consulta por numero de pedido
2: Consulta por cliente
""",
            to=numero
        )
            
    
            
        
        
    return HttpResponse('Bot WP Saladillo')