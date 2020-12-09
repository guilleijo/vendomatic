from django.test import TestCase

from core.serializers import CoinSerializer, InventorySerializer
from core.tests.factories import InventoryFactory, MachineFactory


class InventorySerializerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        machine = MachineFactory()
        cls.inventory = InventoryFactory(
            machine=machine,
            beverage_type="T1",
            quantity=3,
        )
        cls.inventory_2 = InventoryFactory(
            machine=machine,
            beverage_type="T2",
            quantity=4,
        )

    def test_serializer_inventory_list_format(self):
        queryset = [self.inventory, self.inventory_2]
        serialized_inventory = InventorySerializer(queryset, many=True).data
        expected_data = [
            {
                "beverage_type": "T1",
                "quantity": 3,
            },
            {
                "beverage_type": "T2",
                "quantity": 4,
            },
        ]

        self.assertEqual(serialized_inventory, expected_data)

    def test_serializer_inventory_detail_format(self):
        serialized_inventory = InventorySerializer(self.inventory).data
        expected_data = {
            "beverage_type": "T1",
            "quantity": 3,
        }

        self.assertEqual(serialized_inventory, expected_data)


class TestCoinSerializer(TestCase):
    def test_invalid_coin_value(self):
        serializer = CoinSerializer(
            data={
                "coin": 2,
            },
        )
        expected_error = "This field must be 1."

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertEqual(str(serializer.errors["coin"][0]), expected_error)

    def test_valid_coin_value(self):
        serializer = CoinSerializer(
            data={
                "coin": 1,
            },
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 0)
