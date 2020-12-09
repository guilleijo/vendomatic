from django.core.exceptions import ValidationError
from django.test import TestCase

from core.models import Machine
from core.tests.factories import InventoryFactory, MachineFactory


class InventoryModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.machine = MachineFactory()

    def test_validate_quantity_is_not_negative(self):
        inventory = InventoryFactory.build(machine=self.machine, quantity=-1)

        with self.assertRaises(ValidationError) as context:
            inventory.full_clean()

        self.assertEqual(len(context.exception.messages), 1)
        self.assertEqual(
            context.exception.messages[0],
            'Ensure this value is greater than or equal to 0.',
        )

    def test_validate_quantity_is_not_more_than_five(self):
        inventory = InventoryFactory.build(machine=self.machine, quantity=6)

        with self.assertRaises(ValidationError) as context:
            inventory.full_clean()

        self.assertEqual(len(context.exception.messages), 1)
        self.assertEqual(
            context.exception.messages[0],
            'Ensure this value is less than or equal to 5.',
        )

    def test_decrease_stock(self):
        inventory = InventoryFactory.build(machine=self.machine, quantity=5)

        updated_quantity = inventory.decrease_stock()
        inventory.refresh_from_db()

        self.assertEqual(updated_quantity, 4)
        self.assertEqual(inventory.quantity, 4)


class MachineModelTestCase(TestCase):
    def setUp(self):
        self.machine = MachineFactory(coins=5)

    def test_machine_is_unique(self):
        new_machine = MachineFactory.build(coins=3)
        new_machine.save()

        self.assertEqual(Machine.objects.count(), 1)
        self.assertEqual(Machine.objects.first().coins, 3)

    def test_return_coins(self):
        returned_coins = self.machine.return_coins()

        self.machine.refresh_from_db()

        self.assertEqual(returned_coins, 5)
        self.assertEqual(self.machine.coins, 0)

    def test_add_coin(self):
        self.assertEqual(self.machine.coins, 5)

        self.machine.add_coin()
        self.machine.refresh_from_db()

        self.assertEqual(self.machine.coins, 6)

    def test_substract_coins(self):
        self.assertEqual(self.machine.coins, 5)

        remaining_coins = self.machine.substract_coins()
        self.machine.refresh_from_db()

        self.assertEqual(remaining_coins, 3)
        self.assertEqual(self.machine.coins, 3)
