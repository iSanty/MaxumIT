from django.urls import path
from .views import ChangePasswordView, conectarse, registrarse, perfil, editar_perfil, ChangePasswordView
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path('login/', conectarse, name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('registrarse/', registrarse, name='registrarse'),
    path('perfil/', perfil, name='perfil'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
    path('perfil/cambiar-contraseña/', ChangePasswordView.as_view(), name='cambiar_password')   
]

