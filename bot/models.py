from django.db import models

# Create your models here.


class Punto(models.Model):
    numero = models.CharField(max_length=255)
    punto = models.CharField(max_length=255)
    