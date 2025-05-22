from .models import Cart,CartIteam
from . views import _cart_id

def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart=Cart.objects.filter(cart_id=_cart_id(request))
            cart_iteams=CartIteam.objects.all().filter(cart=cart[:1])
            for cart_iteam in cart_iteams:
                cart_count+=cart_iteam.quantity
        except Cart.DoesNotExist:
            cart_count=0
    return dict(cart_count=cart_count)