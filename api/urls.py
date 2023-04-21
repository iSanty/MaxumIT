from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
from .api import PedidoParaMailViewSet


#router.register('api', PedidoParaMailViewSet, 'NuevoPedido')


urlpatterns = router.urls
