from django.shortcuts import render
from .models import Punto
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



def bot(request):
    
    if request.method =="POST":
        
        mensaje = request.POST["Body"]
        numero = request.POST["From"]
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