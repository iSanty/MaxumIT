
from django.urls import path
from .views import index_saladillo, monitor, mail_receptor, config_mail_1, sector_pruebas, subir_estado, bajar_estado, panel_chofer, sincronizar, asignar_hr



urlpatterns = [
    path('', index_saladillo, name='index_saladillo' ),
    path('monitor/', monitor, name='monitor' ),
    path('configuracion/', mail_receptor, name='mail_receptor' ),
    path('configuracion/configurar_mail', config_mail_1, name='config_mail_1' ),
    path('control_pedidos/', sector_pruebas, name='sector_pruebas' ),
    path('control_pedidos/subir_estado/<int:id>/', subir_estado, name='subir_estado' ),
    path('control_pedidos/bajar_estado/<int:id>/', bajar_estado, name='bajar_estado' ),
    path('panel_chofer/', panel_chofer, name='panel_chofer' ),
    path('sincronizar/', sincronizar, name='sincronizar' ),
    path('asignar_hr/<int:id>/', asignar_hr, name='asignar_hr' ),
    
    
    
]

