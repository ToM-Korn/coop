from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField(_('Gesamtsumme'))
    total_weight = models.FloatField(_('Gesamtgewicht'))
    fullfilled = models.BooleanField(_('Ausgeliefert'), default=False)

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField(_('Gesamtsumme'))
    total_weight = models.FloatField(_('Gesamtgewicht'))

class BasketElement(models.Model):
    element = models.ForeignKey('stock.ShippingQuantity', on_delete=models.CASCADE)
    amount = models.IntegerField(_('Bestellmenge'))
    total_price = models.FloatField(_('Gesamtsumme'))
    total_weight = models.FloatField(_('Gesamtgewicht'))
    basket = models.ForeignKey(Basket, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)


@receiver(pre_save, sender=BasketElement)
def update_element_totals(sender, instance, **kwargs):
    instance.total_price = int(instance.amount) * instance.element.price
    instance.total_weight = int(instance.amount) * instance.element.amount

@receiver(pre_save, sender=Basket)
@receiver(pre_save, sender=Order)
def update_totals(sender,instance,**kwargs):
    instance.total_price = 0
    instance.total_weight = 0
    for e in instance.basketelement_set.all():
        instance.total_price += e.total_price
        instance.total_weight += e.total_weight