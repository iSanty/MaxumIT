from django.urls import path
from . import views


urlpatterns = [
    path('primer_aviso/', views.primer_mail)
    ]