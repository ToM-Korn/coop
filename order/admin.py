from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Basket)
admin.site.register(BasketElement)
admin.site.register(Order)
