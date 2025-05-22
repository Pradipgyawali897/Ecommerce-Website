from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartIteam
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

def store(request,categoty_slug=None):
    cateogeries=None
    product=None
    if categoty_slug!=None:
        cateogeries=get_object_or_404(Category,slug=categoty_slug)
        product=Product.objects.filter(category=cateogeries,is_avilable=True)
    else:
        product=Product.objects.all().filter(is_avilable=True)
    paginator=Paginator(product,6)
    page=request.GET.get("page")
    pagged_product=paginator.get_page(page)
    count=product.count()
    return render(request,'store/store.html',context={'products':pagged_product ,'count':count})

def product_detail(request,categoty_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=categoty_slug,slug=product_slug)
        in_cart=CartIteam.objects.filter(cart__cart_id=_cart_id(request),product=single_product)
    except Exception as e:
        raise e
    return render(request,'store/product_detail.html',context={"product":single_product,"in_cart":in_cart})