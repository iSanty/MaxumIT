from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from saladillo.models import PedidoParaMail

from django.conf import settings
from django.core.mail import send_mail

from saladillo.models import PedidoParaMail

import smtplib
import os




@require_POST
def primer_mail(request, *args, **kwargs):
    
    
    if request.method == 'POST':
        
        cliente = request.GET.get('cliente','')
        nro_pedido = request.GET.get('nro_pedido','')
        mail = request.GET.get('mail','')
        
        
        pedido_existente = PedidoParaMail.objects.filter(nro_pedido=nro_pedido)
        if not pedido_existente:
            nuevo_pedido = PedidoParaMail(cliente=cliente,
                                        nro_pedido=nro_pedido,
                                        mail=mail,
                                        mail1_enviado=1,
                                        )
            
            asunto = 'Aviso de recepcion de pedido'
            body = 'Subject: {}\n\n{}'.format(asunto, """Estimado cliente: 
                                    
                                    """+ cliente +
                                    
                                    
                                    """Su pedido nro: """ + nro_pedido + " ha ingresado en nuestro sistema.")
            
            
            server = smtplib.SMTP('smtp.office365.com','587')
            server.starttls()
            server.login(os.getenv('EMAIL_HOST_USER'),os.getenv('EMAIL_HOST_PASSWORD')) #aca logeo
            server.sendmail(os.getenv('EMAIL_HOST_USER'), str(mail), body) #aca uso mi cuenta para q no aparezca "desconocido"
            server.quit()
            
            nuevo_pedido.save()
            
            
            
            return HttpResponse('Success')
        
        else:
            return HttpResponse('Pedido Existente')