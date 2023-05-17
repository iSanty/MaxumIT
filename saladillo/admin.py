from django.contrib import admin

from .models import PedidoParaMail, MaestroCliente, Estados
# Register your models here.


admin.site.register(PedidoParaMail)

admin.site.register(MaestroCliente)


admin.site.register(Estados)