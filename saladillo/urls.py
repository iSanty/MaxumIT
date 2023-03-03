
from django.urls import path
from .views import index_saladillo



urlpatterns = [
    path('', index_saladillo, name='index_saladillo' ),
    
    
]
