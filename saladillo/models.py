from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.




class PedidoParaMail(models.Model):
    cliente = models.CharField(max_length=128)
    nro_pedido = models.IntegerField()
    nro_packing = models.IntegerField(null=True)
    nro_ruteo = models.IntegerField(null=True)
    mail = models.EmailField()
    mail1_enviado = models.BooleanField(null=True)
    mail2_enviado = models.BooleanField(null=True)
    mail3_enviado = models.BooleanField(null=True)
    entregado = models.BooleanField(null=True)
    
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
    
    
    
