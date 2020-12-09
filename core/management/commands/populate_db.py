from django.core.management.base import BaseCommand

from core.models import Inventory, Machine


class Command(BaseCommand):
    help = 'Populates db with a machine and inventory'

    def handle(self, *args, **kwargs):
        # Clean db
        if Machine.objects.exists():
            self.stdout.write('Deleting machine...')
            Machine.objects.all().delete()

        if Inventory.objects.exists():
            self.stdout.write('Deleting inventory...')
            Inventory.objects.all().delete()

        # Populate db
        self.stdout.write('Populating db...')
        machine = Machine.objects.create(pk=1)
        Inventory.objects.create(
            pk=1,
            machine=machine,
            beverage_type='T1',
            quantity=5,
        )
        Inventory.objects.create(
            pk=2,
            machine=machine,
            beverage_type='T2',
            quantity=5,
        )
        Inventory.objects.create(
            pk=3,
            machine=machine,
            beverage_type='T3',
            quantity=5,
        )
        self.stdout.write('Done!')
