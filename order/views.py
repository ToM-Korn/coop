from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, resolve_url
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.

from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic
from .models import Basket, BasketElement, Order
from stock.models import Article, ShippingQuantity

def home(request):
    if request.user.is_authenticated:
        print(request.user.__class__)
        article_list = Article.objects.all()
        user_basket, created = Basket.objects.get_or_create(user=request.user)
        user_order, created = Order.objects.get_or_create(user=request.user)
        return render(request, 'home.html', {'article_list': article_list,
                                             'user_basket': user_basket,
                                             'user_order': user_order})
    return render(request, 'home.html')

@login_required()
@permission_required('is_staff')
def order_overview(request):
    orders = Order.objects.all()
    total_price = 0
    total_weight = 0
    for o in orders:
        total_price += o.total_price
        total_weight += o.total_weight

    article_list = {}

    return render(request,
                  'order_overview.html',
                  {'orders':orders,
                    'total_weight':total_weight,
                    'total_price':total_price,
                    'artile_list': article_list})

@login_required()
def set_order(request):
    # we check if there is a open order that is not fullfilled yet.
    # if this is the case we just update this else
    # we create a new order and move the elements from basket to order

    order = None
    try:
        order = Order.objects.get(user=request.user.id, fullfilled=False)
    except:
        order = Order()
        order.user = request.user
    order.save()

    basket = Basket.objects.get(user=request.user.id)

    for be in basket.basketelement_set.all():
        be.basket = None
        be.order = order
        be.save()

    order.save()
    basket.save()

    return redirect(resolve_url('home'))

@login_required()
def basket_add(request, article_id, shipping_quant_id):
    if request.method == 'POST':
        data = request.POST
        amount = data['order_quant']

    article_quant = get_object_or_404(ShippingQuantity, pk=shipping_quant_id, article=article_id)
    current_user = request.user

    basket, created = Basket.objects.get_or_create(user=current_user)

    be = BasketElement()
    be.amount = amount
    be.basket = basket
    be.element = article_quant
    be.save()

    basket.save()

    return redirect(resolve_url('home'))

@login_required()
def basket_remove(request, basket_item_id):
    be = BasketElement.objects.get(pk=basket_item_id)
    basket = be.basket
    be.delete()

    basket.save()

    return redirect(resolve_url('home'))
