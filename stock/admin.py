from django.contrib import admin

# Register your models here.
from .models import *

class ShippingQuantityInline(admin.TabularInline):
    model = ShippingQuantity

    readonly_fields = ['price_per_unit']


class ArticleAdmin(admin.ModelAdmin):
    inlines = [ShippingQuantityInline]


class ArticleInline(admin.TabularInline):
    model = Article


class SupplierAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]


class GroupAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]

admin.site.register(Article, ArticleAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Origin)
admin.site.register(Brand)
admin.site.register(ShippingQuantity)
