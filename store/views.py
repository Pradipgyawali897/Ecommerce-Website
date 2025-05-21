from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category

def store(request,categoty_slug=None):
    cateogeries=None
    product=None
    if categoty_slug!=None:
        cateogeries=get_object_or_404(Category,slug=categoty_slug)
        product=Product.objects.filter(category=cateogeries,is_avilable=True)
    else:
        product=Product.objects.all().filter(is_avilable=True)
    count=product.count()
    return render(request,'store/store.html',context={'products':product ,'count':count})

def product_detail(request,categoty_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=categoty_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'store/product_detail.html',context={"product":single_product})