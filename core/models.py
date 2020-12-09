from django.db import models
from django.utils.translation import gettext_lazy as _


class Machine(models.Model):
    coins = models.PositiveIntegerField(default=0)


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
