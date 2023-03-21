
from django.urls import path
from .views import index_saladillo, monitor



urlpatterns = [
    path('', index_saladillo, name='index_saladillo' ),
    path('monitor', monitor, name='monitor' ),
    
    
    
]

