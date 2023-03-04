from rest_framework import serializers

from saladillo.models import PedidoParaMail

class PedidoParaMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoParaMail
        fields = ('id', 'cliente', 'nro_pedido', 'mail')
        