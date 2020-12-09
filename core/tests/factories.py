from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from core.models import Machine, Inventory, Beverage

BEVERAGE_TYPES = [beverage for beverage in Beverage]


class MachineFactory(DjangoModelFactory):
    coins = Faker('random_int', min=0, max=50)

    class Meta:
        model = Machine


class InventoryFactory(DjangoModelFactory):
    machine = SubFactory(MachineFactory)
    beverage_type = Faker('random_element', elements=BEVERAGE_TYPES)
    quantity = Faker('random_int', min=0, max=5)

    class Meta:
        model = Inventory
