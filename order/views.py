from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, resolve_url

# Create your views here.

from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic
from .models import Basket, BasketElement
from stock.models import Article, ShippingQuantity

def home(request):
    if request.user.is_authenticated:
        print(request.user.__class__)
        article_list = Article.objects.all()
        user_basket = Basket.objects.get(user=request.user)
        return render(request, 'home.html', {'article_list': article_list, 'user_basket': user_basket})
    return render(request, 'home.html')

def set_order(request):
    return redirect(resolve_url('home'))

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

def basket_remove(request, basket_item_id):
    be = BasketElement.objects.get(pk=basket_item_id)
    basket = be.basket
    be.delete()

    basket.save()

    return redirect(resolve_url('home'))
