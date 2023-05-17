
from django.urls import path
from .views import index_saladillo, monitor, mail_receptor, config_mail_1, sector_pruebas, subir_estado, bajar_estado



urlpatterns = [
    path('', index_saladillo, name='index_saladillo' ),
    path('monitor', monitor, name='monitor' ),
    path('configuracion', mail_receptor, name='mail_receptor' ),
    path('configuracion/configurar_mail', config_mail_1, name='config_mail_1' ),
    path('configuracion/sector_pruebas', sector_pruebas, name='sector_pruebas' ),
    path('configuracion/sector_pruebas/subir_estado/<int:id>/', subir_estado, name='subir_estado' ),
    path('configuracion/sector_pruebas/bajar_estado/<int:id>/', bajar_estado, name='bajar_estado' ),
    
    
    
]

