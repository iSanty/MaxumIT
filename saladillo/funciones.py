
from .models import PrimeraInstancia, MailReceptor

from django.core.mail import send_mail

import smtplib
import os


def mail_primera_instancia(cliente, importe_total, mail, orden_de_compra, nro_pedido, ins1, ins2, ins3, estado):
    
    
    informacion = PrimeraInstancia(
        
        para = mail,
        cliente = cliente,
        valor_total = importe_total,
        orden_de_compra = orden_de_compra,
        nro_pedido = nro_pedido
        
        
        
    )
    
    informacion.body = 'Estimado cliente: ' + cliente + '. Hemos registrado la OC ' + str(orden_de_compra) + ' bajo el nro de pedido: ' + str(nro_pedido) + """
        Por cualquier consulta por favor comunicarse al 0800-xxx-zzzz
        Muchas gracias por su pedido.
        """ 
    
    if ins1 == 'No':
        asunto = 'Aviso de recepcion de pedido'
        body = 'Subject: {}\n\n{}'.format(asunto, """Estimado cliente: 
                                
                                """+ """""" + str(cliente) +""": """+
                                
                                
                                """Su pedido nro: """ + str(nro_pedido) + " ha sido registrado en nuestro sistema." + """
                                Para mas informacion envie un msj de whatsapp al nro: 1153xxxxxx""")
        
        
        
        mail_receptor = MailReceptor.objects.get(id=1)
        server = smtplib.SMTP('smtp.office365.com','587')
        
        server.starttls()
        server.login(os.getenv('EMAIL_HOST_USER'),os.getenv('EMAIL_HOST_PASSWORD')) #aca logeo
        server.sendmail(os.getenv('EMAIL_HOST_USER'), str(mail_receptor), body) #aca uso mi cuenta para q no aparezca "desconocido"
        print('envie')
        server.quit()
        
        
    elif ins1 == 'Si' and ins2 == 'No' and ins3=='No':
        asunto = 'Aviso de preparacion de pedido'
        body = 'Subject: {}\n\n{}'.format(asunto, """Estimado cliente: 
                                
                                """+ """""" + str(cliente) +""": """+
                                
                                
                                """Su pedido nro: """ + str(nro_pedido) + " ya se encuentra preparado." + """
                                Para conocer el detalle envie un msj de whatsapp al nro: 1153xxxxxx""")
        
        
        
        mail_receptor = MailReceptor.objects.get(id=1)
        server = smtplib.SMTP('smtp.office365.com','587')
        
        server.starttls()
        server.login(os.getenv('EMAIL_HOST_USER'),os.getenv('EMAIL_HOST_PASSWORD')) #aca logeo
        server.sendmail(os.getenv('EMAIL_HOST_USER'), str(mail_receptor), body) #aca uso mi cuenta para q no aparezca "desconocido"
        print('envie')
        server.quit()
        
        
    elif ins1 == 'Si' and ins2 == 'Si' and ins3=='No':
        asunto = 'Aviso distribucion de pedido'
        body = 'Subject: {}\n\n{}'.format(asunto, """Estimado cliente: 
                                
                                """+ """""" + str(cliente) +""": """+
                                
                                
                                """Su pedido nro: """ + str(nro_pedido) + " se encuentra en distribucion." + """
                                Para conocer el detalle envie un msj de whatsapp al nro: 1153xxxxxx""")
        
        
        
        mail_receptor = MailReceptor.objects.get(id=1)
        server = smtplib.SMTP('smtp.office365.com','587')
        
        server.starttls()
        server.login(os.getenv('EMAIL_HOST_USER'),os.getenv('EMAIL_HOST_PASSWORD')) #aca logeo
        server.sendmail(os.getenv('EMAIL_HOST_USER'), str(mail_receptor), body) #aca uso mi cuenta para q no aparezca "desconocido"
        print('envie')
        server.quit()
    
    
    
    
    
    
    
    
    
    
    informacion.save()
    
    
    
    
    
    return True



