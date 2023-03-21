
from .models import PrimeraInstancia


def mail_primera_instancia(cliente, importe_total, mail, orden_de_compra, nro_pedido):
    
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
    
    informacion.save()
    
    return True