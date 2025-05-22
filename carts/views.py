from django.shortcuts import render, redirect,get_object_or_404
from .models import Product, Cart, CartIteam


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:  
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()
    try:
        cart_iteam = CartIteam.objects.get(product=product, cart=cart)
        cart_iteam.quantity += 1
        cart_iteam.save()
    except CartIteam.DoesNotExist:
        cart_iteam = CartIteam.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_iteam.save()
    return redirect('cart')

def cart(request,total=0,quantatity=0,cart_iteams=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_iteams=CartIteam.objects.filter(cart=cart,is_active=True)
        for cart_iteam in cart_iteams:
            total+=(cart_iteam.product.price * cart_iteam.quantity)
            quantatity += cart_iteam.quantity
    except :
        pass
    return render(request, 'store/cart.html',context={"total":total,'quantatity':quantatity,"cart_iteams":cart_iteams})

def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    cart_item=CartIteam.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_iteam(request,product_id):
    product = Product.objects.get(id=product_id)
    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_iteam=CartIteam.objects.get(product=product,cart=cart)
    cart_iteam.delete()
    return redirect('cart')