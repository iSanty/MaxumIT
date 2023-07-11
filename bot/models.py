from django.db import models

# Create your models here.


class Punto(models.Model):
    numero = models.CharField(max_length=255)
    punto = models.CharField(max_length=255)
    cons_pedido = models.IntegerField()
    
    def __str__(self):
        return f'{self.numero}'
    
    
    
    
    


class Provisorio(models.Model):
    numero = models.CharField(max_length=128, null=True)
    nombre = models.CharField(max_length=128, null=True)
    apellido = models.CharField(max_length=128, null=True)
    cuit = models.CharField(max_length=128, null=True)
    nro_cliente = models.CharField(max_length=128, null=True)
    alta = models.CharField(max_length=2, null=True)
    instancia = models.CharField(max_length=128, null=True)
    
    
    def __str__(self):
        return f'{self.numero}'
    

    