
from django.urls import path
from .views import index_saladillo, monitor, mail_receptor, config_mail_1



urlpatterns = [
    path('', index_saladillo, name='index_saladillo' ),
    path('monitor', monitor, name='monitor' ),
    path('configuracion', mail_receptor, name='mail_receptor' ),
    path('configuracion/configurar_mail', config_mail_1, name='config_mail_1' ),
    
    
    
]

