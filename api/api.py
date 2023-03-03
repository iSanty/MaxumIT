from saladillo.models import PedidoParaMail
from rest_framework import viewsets, permissions
from .serializers import PedidoParaMailSerializer


class PedidoParaMailViewSet(viewsets.ModelViewSet):
    queryset = PedidoParaMail.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PedidoParaMailSerializer