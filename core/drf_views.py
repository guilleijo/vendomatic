from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import Inventory, Machine
from core.serializers import CoinSerializer, InventorySerializer


class InventoryListAPIView(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [AllowAny]


class InventoryDetailAPIView(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, pk=None):
        beverage = get_object_or_404(self.queryset, pk=pk)
        balance = beverage.machine.coins

        headers = {
            'X-Coins': beverage.machine.coins,
        }

        if beverage.quantity == 0:
            return Response(status=status.HTTP_404_NOT_FOUND, headers=headers)

        if balance < settings.PURCHASE_PRICE:
            return Response(status=status.HTTP_400_BAD_REQUEST, headers=headers)

        with transaction.atomic():
            remaining_coins = beverage.machine.substract_coins()
            remaining_quantity = beverage.decrease_stock()

        serializer = InventorySerializer(beverage)
        headers['X-Coins'] = remaining_coins
        headers['X-Inventory-Remaining'] = remaining_quantity

        return Response(data=serializer.data, headers=headers)


class CoinAPIView(generics.GenericAPIView):
    serializer_class = CoinSerializer
    permission_classes = [AllowAny]

    def put(self, request, pk=None):
        serializer = CoinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        machine = Machine.objects.first()
        machine.add_coin()

        headers = {
            'X-Coins': machine.coins,
        }

        return Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

    def delete(self, request, pk=None):
        machine = Machine.objects.first()
        coins_to_return = machine.return_coins()

        headers = {
            'X-Coins': coins_to_return,
        }

        return Response(status=status.HTTP_204_NO_CONTENT, headers=headers)
