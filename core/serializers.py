from rest_framework import serializers

from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'beverage_type', 'quantity']


class CoinSerializer(serializers.Serializer):
    coin = serializers.IntegerField(required=True)

    def validate_coin(self, value):
        """
        Check that `coin` is 1.
        """
        if value != 1:
            raise serializers.ValidationError('This field must be 1.')
        return value
