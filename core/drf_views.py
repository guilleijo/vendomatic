from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.response import Response

from core.models import Inventory, Machine
from core.serializers import CoinSerializer, InventorySerializer


class InventoryListAPIView(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class InventoryDetailAPIView(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

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

        if balance < 2:
            return Response(status=status.HTTP_400_BAD_REQUEST, headers=headers)

        beverage.machine.coins -= 2
        beverage.machine.save()

        beverage.quantity -= 1
        beverage.save()

        serializer = InventorySerializer(beverage)
        headers['X-Coins'] = beverage.machine.coins
        headers['X-Inventory-Remaining'] = beverage.quantity

        return Response(data=serializer.data, headers=headers)


class CoinAPIView(generics.GenericAPIView):
    serializer_class = CoinSerializer

    def put(self, request, pk=None):
        serializer = CoinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        machine = Machine.objects.first()
        machine.coins += 1
        machine.save()

        headers = {
            'X-Coins': machine.coins,
        }

        return Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

    def delete(self, request, pk=None):
        machine = Machine.objects.first()

        headers = {
            'X-Coins': machine.coins,
        }

        machine.coins = 0
        machine.save()

        return Response(status=status.HTTP_204_NO_CONTENT, headers=headers)