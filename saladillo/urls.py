
from django.urls import path
from .views import index_saladillo, monitor, mail_receptor



urlpatterns = [
    path('', index_saladillo, name='index_saladillo' ),
    path('monitor', monitor, name='monitor' ),
    path('mail-receptor', mail_receptor, name='mail_receptor' ),
    
    
    
]

