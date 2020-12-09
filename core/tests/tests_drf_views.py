from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.tests.factories import InventoryFactory, MachineFactory


"""
GET /inventory -> 200, array of inventory items
GET /inventory/:id -> 200, remaining item quantity

PUT /inventory/:id -> 200, number of coins remaining, item quantity remaining
PUT /inventory/:id -> 404, number of coins accepted
PUT /inventory/:id -> 400, X-Coins:$[0 | 1]

PUT / body: {"coin": 1} -> 204, accepted coins
DELETE / -> 204, returned coins
"""


class InventoryListAPIViewTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.machine = MachineFactory()
        cls.url = reverse('api:inventory-list')

    def test_get_inventory_list(self):
        InventoryFactory(
            machine=self.machine,
            beverage_type="T1",
            quantity=3,
        )
        InventoryFactory(
            machine=self.machine,
            beverage_type="T2",
            quantity=5,
        )

        expected_data = [
            {"beverage_type": "T1", "quantity": 3},
            {"beverage_type": "T2", "quantity": 5},
        ]

        response = self.client.get(self.url)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data, expected_data)


class InventoryDetailAPIViewTestCase(APITestCase):
    def setUp(self):
        self.machine = MachineFactory(coins=3)
        self.inventory = InventoryFactory(
            machine=self.machine,
            beverage_type="T1",
            quantity=3,
        )
        self.url = reverse('api:inventory-detail', kwargs={'pk': self.inventory.pk})

    def test_get_inventory_detail(self):
        expected_data = {"beverage_type": "T1", "quantity": 3}

        response = self.client.get(self.url)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, expected_data)

    def test_buy_beverage_success(self):
        expected_data = {"beverage_type": "T1", "quantity": 2}

        response = self.client.put(self.url)
        response_data = response.json()
        x_coins_header = response.get('X-Coins')
        x_inventory_header = response.get('X-Inventory-Remaining')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(x_coins_header, '1')
        self.assertEqual(x_inventory_header, '2')
        self.assertEqual(response_data, expected_data)

    def test_buy_beverage_no_stock(self):
        self.inventory.quantity = 0
        self.inventory.save()

        response = self.client.put(self.url)
        x_coins_header = response.get('X-Coins')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(x_coins_header, '3')

    def test_buy_beverage_no_funds_0(self):
        self.machine.coins = 0
        self.machine.save()

        response = self.client.put(self.url)
        x_coins_header = response.get('X-Coins')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(x_coins_header, '0')

    def test_buy_beverage_no_funds_1(self):
        self.machine.coins = 1
        self.machine.save()

        response = self.client.put(self.url)
        x_coins_header = response.get('X-Coins')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(x_coins_header, '1')


class CoinAPIViewTestCase(APITestCase):
    def setUp(self):
        self.machine = MachineFactory(coins=0)
        self.url = reverse('api:coin')

    def test_add_coin_1(self):
        self.assertEqual(self.machine.coins, 0)
        data = {'coin': 1}

        response = self.client.put(self.url, data)
        x_coins_header = response.get('X-Coins')
        self.machine.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(x_coins_header, '1')
        self.assertEqual(self.machine.coins, 1)

    def test_add_coin_invalid(self):
        data = {'coin': 2}
        expected_msg = {'coin': ['This field must be 1.']}

        response = self.client.put(self.url, data)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, expected_msg)

    def test_get_coins_back(self):
        self.machine.coins = 4
        self.machine.save()

        response = self.client.delete(self.url)
        x_coins_header = response.get('X-Coins')
        self.machine.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(x_coins_header, '4')
        self.assertEqual(self.machine.coins, 0)
