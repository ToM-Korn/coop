from django.urls import path

from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('add_to_basket/<int:article_id>/<int:shipping_quant_id>', basket_add, name='add_to_basket'),
    path('remove_from_basket/<int:basket_item_id>', basket_remove, name='remove_from_basket'),
    path('set_order', set_order, name='set_order'),
    path('order_overview', order_overview, name='order_overview'),
    path('basket', basket, name='basket'),
    path('order', order, name='order')
]
