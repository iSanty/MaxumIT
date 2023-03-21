from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.




class PedidoParaMail(models.Model):
    codigo_cliente = models.IntegerField()
    cliente = models.CharField(max_length=128)
    nro_pedido = models.IntegerField()
    nro_packing = models.IntegerField(null=True)
    nro_ruteo = models.IntegerField(null=True)
    mail = models.EmailField(null=True)
    mail1_enviado = models.BooleanField(null=True)
    mail2_enviado = models.BooleanField(null=True)
    mail3_enviado = models.BooleanField(null=True)
    entregado = models.BooleanField(null=True)
    cantidad = models.IntegerField()
    importe_total = models.IntegerField()
    orden_de_compra = models.CharField(max_length=128)
    
    fecha_creacion = models.DateField(null=True)
    
    
    def __str__(self):
        return f'{self.nro_pedido} - {self.cliente}'
    
        
        
    
class ConfiguracionMail(models.Model):
    servidor_pop = models.CharField(max_length=128)
    puerto_servidor = models.CharField(max_length=10)
    
    def __str__(self):
        return f'{self.servidor_pop} - {self.puerto_servidor}'
    
    
class CuerpoMail(models.Model):
    instancia = models.IntegerField()
    body = RichTextField(max_length=512)
    
    
    def __str__(self):
        return f'{self.body}'
    
    
    


class MaestroCliente(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=128)
    domicilio = models.CharField(max_length=128)
    localidad = models.CharField(max_length=128)
    cod_loc = models.IntegerField()
    provincia = models.CharField(max_length=128)
    telefono = models.CharField(max_length=128)
    cuit = models.CharField(max_length=128)
    cond_iva = models.CharField(max_length=128)
    
    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
    
    
    
    
    
class PrimeraInstancia(models.Model):
    para = models.EmailField(null=True)
    de = models.EmailField(null=True)
    cliente = models.CharField(max_length=128)
    body = RichTextField(max_length=1024)
    nro_pedido = models.IntegerField()
    orden_de_compra = models.CharField(max_length=128)
    valor_total = models.IntegerField()
    
    
    def __str__(self):
        return f'{self.nro_pedido}'