from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Machine(models.Model):
    coins = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def return_coins(self):
        accepted_coins = self.coins
        self.coins = 0
        self.save()
        return accepted_coins

    def add_coin(self):
        self.coins += 1
        self.save()

    def substract_coins(self):
        self.coins -= settings.PURCHASE_PRICE
        self.save()
        return self.coins


class Beverage(models.TextChoices):
    TYPE_ONE = 'T1', _('Type one')
    TYPE_TWO = 'T2', _('Type two')
    TYPE_THREE = 'T3', _('Type three')


class Inventory(models.Model):
    machine = models.ForeignKey(
        Machine,
        related_name='inventory',
        on_delete=models.CASCADE,
    )
    beverage_type = models.CharField(
        max_length=2,
        choices=Beverage.choices,
        null=True,
        blank=True,
        default=None,
    )
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = _('Inventory')
        unique_together = ('machine', 'beverage_type')

    def decrease_stock(self):
        self.quantity -= 1
        self.save()
        return self.quantity
