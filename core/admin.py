from django.contrib import admin

from .models import Inventory, Machine


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'beverage_type',
        'quantity',
    )


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'coins'
    )
