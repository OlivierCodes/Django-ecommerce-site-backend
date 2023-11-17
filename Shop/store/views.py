
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from datetime import datetime

from django.urls import reverse
from store.models import Cart, Order, Product

# Aceuil du site 
def index(resuest):
    products = Product.objects.all()
    return render(resuest, 
                  'store/index.html',
                  context={"products": products})

# Détail du produit
def product_detail(request, slug):
    date = datetime.today()
    product = get_object_or_404(Product, 
                                slug=slug)
    
    return render(request, 
                  'store/detail.html',
                    context={"product": product,
                             "date":date})

def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)

    cart, _ = Cart.objects.get_or_create(user=user)

    order, created = Order.objects.get_or_create(user=user,
                                                ordered = False,
                                                  product=product)
    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()
    return redirect(reverse("product", 
                            kwargs={"slug":slug}))


def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 
                  'store/cart.html',
                  context={"orders":cart.orders.all()})

def delete_cart(request):
    cart = request.user.cart
    if cart:
        cart.orders.all().delete()
        cart.delete()
    return redirect('index')



