from django.contrib import admin

# Register your models here.

from .models import pedidos, clientes_emails
admin.site.register(pedidos)
admin.site.register(clientes_emails)