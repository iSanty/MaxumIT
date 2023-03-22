from django.db import models
from datetime import datetime, date
# Create your models here.

class pedidos(models.Model):
    
    numero = models.IntegerField(primary_key=True)
    fecha = models.DateField(null=date.today())
    codigo_cliente = models.IntegerField()
    codigo_articulo = models.CharField(max_length=128)
    cantidad = models.IntegerField()
    importe = models.IntegerField()
    importe_total_comprobante = models.IntegerField()
    fechavencimiento1 = models.DateField(null=True)
    ordendecompra = models.CharField(max_length=128)
    fecha_entrega = models.DateField(null=True)

    
    def __str__(self):
        return f'{self.numero} - {self.codigo_articulo}'
    
    
    
    
    
class clientes_emails(models.Model):
    codigo = models.IntegerField(primary_key=True, db_column='código')
    nombre = models.CharField(max_length=128)
    email_1 = models.EmailField(db_column='email 1')
    email_2 = models.EmailField(db_column='email 2')
    email_3 = models.EmailField(db_column='email 3')
    
    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
    
    
