from django.db import models

from django.contrib.auth.models import User
from ckeditor.fields import RichTextField



class MasDatosUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatares', null=True, blank =True)
    descripcion = RichTextField(null=True)
    num_celular = models.CharField(max_length=128)
    codigo_cliente = models.IntegerField(null=True)
    
    def __str__(self):
        return f'{self.user}'
    
