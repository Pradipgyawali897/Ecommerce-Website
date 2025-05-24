from django.shortcuts import render,get_object_or_404
from .models import Product,Variation
from category.models import Category
from carts.models import CartIteam
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


def pagination_creator(product,request):
    paginator=Paginator(product,6)
    page=request.GET.get("page")
    pagged_product=paginator.get_page(page)
    return pagged_product

def store(request,categoty_slug=None):
    cateogeries=None
    product=None
    if categoty_slug!=None:
        cateogeries=get_object_or_404(Category,slug=categoty_slug)
        product=Product.objects.filter(category=cateogeries,is_avilable=True)
    else:
        product=Product.objects.all().filter(is_avilable=True).order_by('id')
    pagged_product=pagination_creator(product=product,request=request)
    count=product.count()
    return render(request,'store/store.html',context={'products':pagged_product ,'count':count})

def product_detail(request, categoty_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=categoty_slug, slug=product_slug)
        in_cart = CartIteam.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    colour = Variation.objects.filter(product=single_product, variation_category="colour", is_active=True)
    size = Variation.objects.filter(product=single_product, variation_category="size", is_active=True)
    return render(request, 'store/product_detail.html', context={"product": single_product, "in_cart": in_cart, "colour": colour, "size": size})

def search_view(request):
    q=request.GET.get('q')
    product=Product.objects.filter(Q(product_name__icontains=q)  | Q(product_description__icontains=q)).order_by('-created_date')
    pagged_product=pagination_creator(product=product,request=request)
    count=product.count()
    return render(request,'store/store.html',context={'products':pagged_product ,'count':count})
