from django.contrib import admin

from .models import PedidoParaMail, MaestroCliente, Estados, NroPruebaBot, ConfiguracionMail, CuerpoMail, MaestroCliente, PrimeraInstancia, MailReceptor, HojaRuta
# Register your models here.


admin.site.register(PedidoParaMail)

admin.site.register(MaestroCliente)


admin.site.register(Estados)

admin.site.register(NroPruebaBot)

admin.site.register(ConfiguracionMail)

admin.site.register(CuerpoMail)

admin.site.register(MailReceptor)

admin.site.register(PrimeraInstancia)


admin.site.register(HojaRuta)