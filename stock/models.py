from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.db import models
from django.utils.translation import gettext as _

UNITS = [
    ('kg', _("Kilogramm")),
    ('lt', _("Liter"))
]

# WGr	                Artikel	  Aktiv	Lieferant	    Marke	        Herkunft	LE	Inhalt	Preis/ LE	Preis/kg
#Back und Bindemittel	Agar Agar		Nestelberger	Nestelberger	kbA	        kg	0,050	3,63	72,60

class Group(models.Model):
    name = models.CharField(_('Bezeichnung'), max_length=200, null=False)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(_('Name'), max_length=200, null=False)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(_('Name'), max_length=200, null=False)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Origin(models.Model):
    name = models.CharField(_('Herkunftsort'), max_length=200, null=False)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(_('Bezeichnung'), max_length=200, null=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
    active = models.BooleanField(_('Aktiv'),default=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    origin = models.ForeignKey(Origin, on_delete=models.SET_NULL, null=True, blank=True)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class ShippingQuantity(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, parent_link=True, null=False, blank=False)
    amount = models.FloatField(_('Menge'), null=False, blank=False)
    packaging_unit = models.CharField(_('Verpackungseinheit'), max_length=20, choices=UNITS, null=False)
    price = models.FloatField(_('Preis'), null=False, blank=False)
    price_per_unit = models.FloatField(_('Preis pro Verpackungseinheit'),
                                       null=True,
                                       blank=True,
                                       help_text=_('Wird automatisch gesetzt'))

    def __str__(self):
        return str(self.amount) + " " + self.packaging_unit + " " + self.article.name


@receiver(pre_save, sender=ShippingQuantity)
def calculate_price_per_unit(sender,instance,**kwargs):
    instance.price_per_unit = instance.price / instance.amount
