from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class Estados(models.Model):
    estado = models.CharField(max_length=128)
    
    def __str__(self):
        return f'{self.estado}'
        

class PedidoParaMail(models.Model):
    codigo_cliente = models.IntegerField(null=True)
    cliente = models.CharField(max_length=128, null=True)
    nro_pedido = models.IntegerField(null=True)
    nro_packing = models.IntegerField(null=True)
    nro_ruteo = models.IntegerField(null=True)
    mail = models.EmailField(null=True)
    mail1_enviado = models.CharField(max_length=12,null=True)
    mail2_enviado = models.CharField(max_length=12,null=True)
    mail3_enviado = models.CharField(max_length=12,null=True)
    entregado = models.CharField(max_length=126,null=True)
    cantidad = models.IntegerField(null=True)
    importe_total = models.IntegerField(null=True)
    orden_de_compra = models.CharField(max_length=128,null=True)
    estado = models.CharField(max_length=128,null=True)
    estado_2 = models.CharField(max_length=128,null=True)
    estado_3 = models.CharField(max_length=128,null=True)
    estado_4 = models.CharField(max_length=128,null=True)

    fecha_creacion = models.DateField(null=True)
    fecha_estado = models.DateField(null=True)
    fecha_estado_2 = models.DateField(null=True)
    fecha_estado_3 = models.DateField(null=True)
    fecha_estado_4 = models.DateField(null=True)
    domicilio = models.CharField(max_length=128, null=True)
    localidad = models.CharField(max_length=128, null=True)
    cp = models.CharField(max_length=128, null=True)
    estado_hr = models.CharField(max_length=128, null=True)
    num_celular = models.CharField(max_length=128, null=True)
    
    def __str__(self):
        return f'{self.nro_pedido} - {self.cliente}'
    
        
        
    
class ConfiguracionMail(models.Model):
    servidor_pop = models.CharField(max_length=128)
    puerto_servidor = models.CharField(max_length=10)
    
    def __str__(self):
        return f'{self.servidor_pop} - {self.puerto_servidor}'
    
    
class CuerpoMail(models.Model):
    instancia = models.IntegerField(null=True)
    body_uno = RichTextField(max_length=512, null=True)
    body_dos = RichTextField(max_length=512, null=True)
    body_tres = RichTextField(max_length=512, null=True)
    body_cuatro = RichTextField(max_length=512, null=True)
    body_cinco = RichTextField(max_length=512, null=True)
    body_seis = RichTextField(max_length=512, null=True)
    body_siete = RichTextField(max_length=512, null=True)
    body_ocho = RichTextField(max_length=512, null=True)
    body_nueve = RichTextField(max_length=512, null=True)
    body_diez = RichTextField(max_length=512, null=True)
    body_once = RichTextField(max_length=512, null=True)
    body_doce = RichTextField(max_length=512, null=True)
    body_trece = RichTextField(max_length=512, null=True)
    body_catorce = RichTextField(max_length=512, null=True)
    
    
    def __str__(self):
        return f'{self.body_uno}'
    
    
    


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
    num_celular = models.CharField(max_length=128)
    
    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
    
    
class DatosCliente(models.Model):
    codigo = models.IntegerField()
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
    
    
    
class MailReceptor(models.Model):
    mail = models.EmailField(max_length=128)
    
    def __str__(self):
        return f'{self.mail}'
    
    
class HojaRuta(models.Model):
    nro_hoja_de_ruta = models.IntegerField()
    nro_pedido = models.IntegerField()
    estado_en_hr = models.CharField(max_length=128)
    transportista = models.CharField(max_length=128)
    
    def __str__(self):
        return f'{self.nro_hoja_de_ruta}'
    
    
class NroPruebaBot(models.Model):
    nro = models.CharField(max_length=14)
    
    
    def __str__(self):
        return f'{self.nro}'
    
    
    
class Articulo(models.Model):
    articulo = models.CharField(max_length=128)
    descripcion = models.CharField(max_length=256)
    
    def __str__(self):
        return f'{self.articulo}'