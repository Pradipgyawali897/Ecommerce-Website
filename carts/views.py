from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from .models import Product, Cart, CartIteam
from store.models import Variation
from django.contrib.messages import success,error
from django.contrib.auth.models import User


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            product = Product.objects.get(id=product_id)
            product_variation = []
            for items in request.POST:
                key = items
                value = request.POST.get(key)
                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value
                    )
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    pass

            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()

            is_cart_iteam_exists = CartIteam.objects.filter(product=product, cart=cart).exists()
            if is_cart_iteam_exists:
                cart_iteam = CartIteam.objects.filter(product=product, cart=cart)
                for item in cart_iteam:
                    existing_variations = list(item.variations.all())
                    if set(product_variation) == set(existing_variations):
                        item.quantity += 1
                        item.save()
                        break
                else:
                    # No matching variations found, create new cart item
                    cart_iteam = CartIteam.objects.create(
                        product=product,
                        quantity=1,
                        cart=cart
                    )
                    if product_variation:
                        cart_iteam.variations.add(*product_variation)
                    cart_iteam.save()
            else:
                # No cart item exists, create new one
                cart_iteam = CartIteam.objects.create(
                    product=product,
                    quantity=1,
                    cart=cart
                )
                if product_variation:
                    cart_iteam.variations.add(*product_variation)
                    success(request,"Added to the cart")
                cart_iteam.save()

            return redirect('cart')
        else:
            error(request,"Logged In first")
            return redirect("register")


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

def remove_cart(request,product_id,cart_iteam_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    cart_item=CartIteam.objects.get(product=product,cart=cart,id=cart_iteam_id)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
        success(request,"The product is removed")
    return redirect('cart')

def remove_cart_iteam(request,product_id,cart_iteam_id):
    product = Product.objects.get(id=product_id)
    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_iteam=CartIteam.objects.get(product=product,cart=cart,id=cart_iteam_id)
    cart_iteam.delete()
    success(request,"The product is removed")
    return redirect('cart')