

from django.urls import path
from .views import leer_saladillo



urlpatterns = [
    path('', leer_saladillo, name='leer_saladillo' ),
    
    
]
